const fs = require("fs");
const path = require("path");

function isDatedJsonFile(fileName) {
  return /^\d{8}\.json$/i.test(fileName);
}

function parseDateFromFileName(fileName) {
  const date = fileName.slice(0, 8);
  const year = Number(date.slice(0, 4));
  const month = Number(date.slice(4, 6));
  const day = Number(date.slice(6, 8));

  // Use UTC to avoid local TZ shifting.
  const dateObj = new Date(Date.UTC(year, month - 1, day));
  return { date, dateObj };
}

function safeJsonParse(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  try {
    return JSON.parse(raw);
  } catch (e) {
    return {
      parse_error: true,
      parse_error_message: String(e && e.message ? e.message : e),
      raw
    };
  }
}

module.exports = function () {
  // Eleventy runs with the repo root as the working directory.
  // We keep the summary JSON files in /content (e.g. content/20260220.json).
  const repoRoot = process.cwd();
  const contentDir = path.join(repoRoot, "content");

  if (!fs.existsSync(contentDir)) {
    return {
      items: [],
      latest: null,
      error: `Missing content directory: ${contentDir}`
    };
  }

  const fileNames = fs
    .readdirSync(contentDir)
    .filter(isDatedJsonFile)
    .sort((a, b) => b.localeCompare(a)); // yyyymmdd string sort works

  const items = fileNames.map((fileName) => {
    const { date, dateObj } = parseDateFromFileName(fileName);
    const fullPath = path.join(contentDir, fileName);
    const data = safeJsonParse(fullPath);

    return {
      fileName,
      displayName: fileName,
      slug: date,
      date,
      dateObj,
      url: `/summary/${date}/`,
      data
    };
  });

  return {
    items,
    latest: items.length > 0 ? items[0] : null
  };
};
