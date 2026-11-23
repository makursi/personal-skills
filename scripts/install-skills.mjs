#!/usr/bin/env node
// 把 skills/ 下的 skill 以目录链接的方式安装到目标目录。
// Windows 用 junction（不需要管理员权限），其他平台用目录符号链接。
// 仓库是唯一真源：链接指回仓库，改了文件立刻生效。
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_DIR = path.join(REPO_ROOT, "skills");
const DEFAULT_TARGET = path.join(os.homedir(), ".agents", "skills");

const USAGE = `用法：node scripts/install-skills.mjs [选项]

  --target <dir>        安装到哪，默认 ${DEFAULT_TARGET}
  --scope <值>          global（默认，装 scope 缺省或 global 的 skill）
                        all      装全部
                        project:<name>  只装 metadata.scope 等于它的 skill
  --dry-run             只打印计划，不写磁盘
  --force               覆盖已存在的真实目录或别人的链接
  --uninstall           删除指回本仓库的链接
  --help, -h            打印这段说明

退出码：0 成功，1 有失败，2 参数问题。
`;

function fail(message) {
  console.error(`错误：${message}`);
  process.exit(2);
}

function parseArgs(argv) {
  const options = {
    target: null,
    scope: "global",
    dryRun: false,
    force: false,
    uninstall: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const equals = arg.indexOf("=");
    const key = equals === -1 ? arg : arg.slice(0, equals);
    const inline = equals === -1 ? null : arg.slice(equals + 1);

    const takeValue = () => {
      if (inline !== null) return inline;
      const next = argv[index + 1];
      if (!next || next.startsWith("--")) fail(`${key} 缺少值`);
      index += 1;
      return next;
    };

    switch (key) {
      case "--target":
        options.target = takeValue();
        break;
      case "--scope":
        options.scope = takeValue();
        break;
      case "--dry-run":
        options.dryRun = true;
        break;
      case "--force":
        options.force = true;
        break;
      case "--uninstall":
        options.uninstall = true;
        break;
      case "--help":
      case "-h":
        options.help = true;
        break;
      default:
        fail(`未知参数 ${arg}`);
    }
  }

  options.target = path.resolve(options.target ?? DEFAULT_TARGET);
  return options;
}

// 只读 SKILL.md 里的 name 和 metadata.scope，不引入 YAML 依赖。
function readMetadata(skillDir) {
  const file = path.join(skillDir, "SKILL.md");
  let text = "";
  try {
    text = fs.readFileSync(file, "utf8");
  } catch {
    return { name: path.basename(skillDir), scope: "global", hasSkillFile: false };
  }

  const frontmatter = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  const front = frontmatter ? frontmatter[1] : "";
  const nameMatch = /^name:\s*["']?([^"'\r\n]+)["']?\s*$/m.exec(front);
  const scopeMatch = /^\s+scope:\s*["']?([^"'\r\n#]+?)["']?\s*$/m.exec(front);

  return {
    name: nameMatch ? nameMatch[1].trim() : path.basename(skillDir),
    scope: scopeMatch ? scopeMatch[1].trim() : "global",
    hasSkillFile: true,
  };
}

function listSkills() {
  if (!fs.existsSync(SKILLS_DIR)) return [];
  return fs
    .readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => {
      const dir = path.join(SKILLS_DIR, entry.name);
      return { dir, dirName: entry.name, ...readMetadata(dir) };
    })
    .sort((left, right) => left.dirName.localeCompare(right.dirName));
}

function existingKind(target) {
  try {
    const stat = fs.lstatSync(target);
    if (stat.isSymbolicLink()) return "link";
    if (stat.isDirectory()) return "directory";
    return "file";
  } catch {
    return "missing";
  }
}

function linkPointsIntoRepo(target) {
  try {
    const resolved = fs.realpathSync(target);
    const repo = fs.realpathSync(REPO_ROOT);
    return resolved === repo || resolved.startsWith(repo + path.sep);
  } catch {
    return false;
  }
}

function matchesScope(skill, scope) {
  if (scope === "all") return true;
  if (scope.startsWith("project:")) return skill.scope === scope;
  return skill.scope === "global";
}

function createLink(source, destination) {
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  const type = process.platform === "win32" ? "junction" : "dir";
  fs.symlinkSync(source, destination, type);
}

function removeLink(target) {
  fs.unlinkSync(target);
}

function installSkill(skill, options, stats) {
  const destination = path.join(options.target, skill.dirName);
  const kind = existingKind(destination);

  if (kind === "link") {
    if (linkPointsIntoRepo(destination)) {
      console.log(`  已安装  ${skill.dirName}`);
      stats.skipped += 1;
      return;
    }
    if (!options.force) {
      console.error(`  冲突    ${skill.dirName}：已存在指向别处的链接，加 --force 覆盖`);
      stats.failed += 1;
      return;
    }
    if (!options.dryRun) removeLink(destination);
    console.log(`  替换    ${skill.dirName}（原有链接指向别处）`);
  } else if (kind === "directory" || kind === "file") {
    if (!options.force) {
      console.error(`  冲突    ${skill.dirName}：目标位置已有真实${kind === "file" ? "文件" : "目录"}，加 --force 覆盖`);
      stats.failed += 1;
      return;
    }
    if (!options.dryRun) fs.rmSync(destination, { recursive: true, force: true });
    console.log(`  覆盖    ${skill.dirName}（删除原有真实${kind === "file" ? "文件" : "目录"}）`);
  }

  const verb = options.dryRun ? "计划" : "安装";
  console.log(`  ${verb}    ${skill.dirName}  ->  ${destination}`);
  if (!options.dryRun) createLink(skill.dir, destination);
  stats.installed += 1;
}

function uninstallSkill(skill, options, stats) {
  const destination = path.join(options.target, skill.dirName);
  const kind = existingKind(destination);

  if (kind === "missing") {
    console.log(`  未安装  ${skill.dirName}`);
    stats.skipped += 1;
    return;
  }
  if (kind !== "link" || !linkPointsIntoRepo(destination)) {
    console.error(`  跳过    ${skill.dirName}：${destination} 不是指回本仓库的链接`);
    stats.failed += 1;
    return;
  }

  const verb = options.dryRun ? "计划删除" : "删除";
  console.log(`  ${verb}  ${skill.dirName}  ${destination}`);
  if (!options.dryRun) removeLink(destination);
  stats.installed += 1;
}

function main() {
  const options = parseArgs(process.argv.slice(2));

  if (options.help) {
    process.stdout.write(USAGE);
    return 0;
  }

  const skills = listSkills();
  if (skills.length === 0) {
    console.log("skills/ 里没有 skill，没有可安装的内容。");
    return 0;
  }

  const selected = skills.filter((skill) => matchesScope(skill, options.scope));
  if (selected.length === 0) {
    console.log(`scope=${options.scope} 没有匹配的 skill。`);
    return 0;
  }

  const missingSkillFile = selected.filter((skill) => !skill.hasSkillFile);
  for (const skill of missingSkillFile) {
    console.error(`  跳过    ${skill.dirName}：缺少 SKILL.md`);
  }

  const usable = selected.filter((skill) => skill.hasSkillFile);
  const stats = { installed: 0, skipped: 0, failed: missingSkillFile.length };

  const action = options.uninstall ? "卸载" : "安装";
  const mode = options.dryRun ? "（试运行，不写磁盘）" : "";
  console.log(`${action}到 ${options.target}${mode}\n`);

  for (const skill of usable) {
    if (options.uninstall) uninstallSkill(skill, options, stats);
    else installSkill(skill, options, stats);
  }

  console.log(
    `\n${options.uninstall ? "卸载" : "安装"}完成：` +
      `成功 ${stats.installed}，跳过 ${stats.skipped}，失败 ${stats.failed}。`
  );
  return stats.failed > 0 ? 1 : 0;
}

process.exit(main());
