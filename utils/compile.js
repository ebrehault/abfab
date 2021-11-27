const svelte = require('svelte/compiler');
const fs = require('fs');

const args = process.argv.slice(2);
const source = args[0];
const ABFAB_ROOT = '/~';
const SVELTE_IMPORTS = new RegExp(/from "(.+\/svelte(\/\w+){0,1})";/g);
const LIB_IMPORTS = new RegExp(/import (.+) from ['"]((?![.\/]|https?:\/\/).+)['"];/g);

fs.readFile(source, 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
    const { js } = svelte.compile(data, {
        sveltePath: ABFAB_ROOT + '/libs/svelte',
        customElement: data.includes('<svelte:options tag='),
    });
    if (js.code) {
        const code = js.code
            .replace(SVELTE_IMPORTS, 'from "$1/index.mjs";')
            .replace(LIB_IMPORTS, 'import $1 from "/~/libs/$2";');
        fs.writeFile(source + '.js', code, function (err) {
            if (err) {
                return console.log(err);
            }
        });
    }
});
