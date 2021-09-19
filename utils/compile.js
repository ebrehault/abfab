const svelte = require('svelte/compiler');
const fs = require('fs');

const args = process.argv.slice(2);
const source = args[0];
const ABFAB_ROOT = '/~';
const RE = new RegExp(/from "(.+\/svelte(\/\w+){0,1})";/g);

fs.readFile(source, 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
    const { js } = svelte.compile(data, {
        sveltePath: ABFAB_ROOT + '/libs/svelte',
    });
    if (js.code) {
        const code = js.code.replace(RE, 'from "$1/index.mjs";');
        fs.writeFile(source + '.js', code, function (err) {
            if (err) {
                return console.log(err);
            }
        });
    }
});
