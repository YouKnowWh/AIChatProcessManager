import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const input = path.resolve("outputs/manual-aichat-complete-ppt/presentations/aichat-process-manager/output/AIChatProcessManager-complete-defense.pptx");
const output = path.resolve("AIChatProcessManager-complete-defense.pptx");
const work = await fs.mkdtemp(path.join(os.tmpdir(), "aichat-pptx-"));

function run(cmd, args, cwd) {
  const result = spawnSync(cmd, args, { cwd, encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(`${cmd} failed\n${result.stdout}\n${result.stderr}`);
  }
}

await fs.copyFile(input, output);
run("unzip", ["-q", output, "-d", work], process.cwd());

const patterns = [
  '<p:transition spd="med" advClick="1"><p:fade/></p:transition>',
  '<p:transition spd="med" advClick="1"><p:push dir="l"/></p:transition>',
  '<p:transition spd="med" advClick="1"><p:wipe dir="r"/></p:transition>',
  '<p:transition spd="slow" advClick="1"><p:fade/></p:transition>',
];

const slideDir = path.join(work, "ppt", "slides");
const slideFiles = (await fs.readdir(slideDir))
  .filter((name) => /^slide\d+\.xml$/.test(name))
  .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));

for (const [index, file] of slideFiles.entries()) {
  const i = index + 1;
  const slidePath = path.join(slideDir, file);
  let xml = await fs.readFile(slidePath, "utf8");
  xml = xml.replace(/<p:transition[\s\S]*?<\/p:transition>/g, "");
  const transition = patterns[(i - 1) % patterns.length];
  xml = xml.replace("</p:sld>", `${transition}</p:sld>`);
  await fs.writeFile(slidePath, xml, "utf8");
}

run("zip", ["-qr", output, "."], work);

const stat = await fs.stat(output);
console.log(JSON.stringify({ output, bytes: stat.size, transitions: slideFiles.length }, null, 2));
