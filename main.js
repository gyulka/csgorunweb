function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
};
http = new XMLHttpRequest();
http.open('GET', 'http://192.168.5.191:5000/get_token',false);
http.send();
console.log(http.responseText);

x = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru,en;q=0.9',
    'authorization': http.responseText,
    'content-length': '22',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://csgorun.gg',
    'referer': 'https://csgorun.gg/',
    'sec-ch-ua': '"Yandex";v="21", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36'
};
x['authorization']=http.responseText
async function get_inv(i) {
    http = new XMLHttpRequest();
    http.open('GET', 'https://api.csgorun.gg/current-state?montaznayaPena=null', false);
    http.setRequestHeader('authorization', x['authorization']);
    http.send();
    let response = JSON.parse(http.responseText);
    inv = response['data']['user']['items'];
    return inv;
}
async function get_balance(){
    http = new XMLHttpRequest();
    http.open('GET', 'https://api.csgorun.gg/current-state?montaznayaPena=null', false);
    http.setRequestHeader('authorization', x['authorization']);
    http.send();
    let response = JSON.parse(http.responseText);
    balance = response['data']['user']['balance'];
    return balance;
}
async function func(ids) {
    let x=0;
    http = new XMLHttpRequest();
    http.open('POST', 'http://192.168.5.191:5000/update_inv');
    http.send(JSON.stringify({ 'userItemIds': ids,'balance':await get_balance()}));
    return http.responseText;
}
async function get_game(i) {
    http = new XMLHttpRequest();
    http.open('GET', 'https://api.csgorun.gg/games/' + i);
    http.send();
    while (http.status != 200) {
        http.open('GET', 'https://api.csgorun.gg/games/' + i);
        http.send();
        await sleep(1000);
    }
    response = JSON.parse(http.responseText)['data']['crash'];
    return response;
}
async function make_bet(lis){
http = new XMLHttpRequest();
    http.open('POST', 'http://192.168.5.191:5000/append');
    http.send(JSON.stringify({ 'id': lis[1],'crash':lis[0]}));
};

async function main(i) {

let lis = [];
while (true) {
    let crash = await get_game(i)
    if (lis.length > 0) {
        if (lis[lis.length - 1][1] != i) {
            lis.push([crash, i]);
        };
    };
    else {
        lis.push([crash, i]);
    }
    if (lis.length > 5) {
        lis.shift();
        console.log(lis[lis.length - 1]);
        if (true) {
            inv = await get_inv();
            func(inv);
            make_bet(lis[lis.length - 1]);
                };
    }
    i=i+1;

}};
inv = await get_inv();
await func(inv);
http = new XMLHttpRequest();
http.open('POST', 'http://192.168.5.191:5000/init',false);
http.send();
inv = await get_inv();
await func(inv);