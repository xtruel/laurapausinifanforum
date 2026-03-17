const https = require('https');
const fs = require('fs');

const download = (url, dest) => {
  return new Promise((resolve, reject) => {
    const options = new URL(url);
    options.headers = {
      'Referer': 'https://laurapausinifanforum.forumcommunity.net/',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    };
    https.get(options, (res) => {
      const file = fs.createWriteStream(dest);
      res.pipe(file);
      file.on('finish', () => {
        file.close(resolve);
      });
    }).on('error', (err) => {
      fs.unlink(dest, () => reject(err));
    });
  });
};

async function main() {
  if (!fs.existsSync('avatars')) fs.mkdirSync('avatars');
  await download('https://uploads.forumcommunity.it/av-12526073.jpg', 'avatars/patricia.jpg');
  await download('https://upload.forumfree.net/i/fc941637/avatar/sissy.png', 'avatars/sissy.png');
  await download('https://uploads.forumcommunity.it/av-941637-1767256489.png', 'avatars/ciccio.png');
  await download('https://uploads.forumcommunity.it/av-12943232-1773678655.jpg', 'avatars/clau.jpg');
  console.log('Avatars downloaded successfully.');
}

main();
