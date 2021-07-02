var tries = 2
var match = ""
var score = 0
var num = 0
var isShiny = false
var rand = 0
var start = 0
var end = 0
var user = 0
var pokeName = ''
var type = ''
var ability = ''

function updateMatch(e){
    match = e.value;
}

function startPoke(s, e){
    start = s;
    end = e;
    randPoke()
    getPoke()
}

function getPoke(){
    fetch("http://localhost:5000/pokemon/recent")
        .then(res => res.json())
        .then(data => {
            if (data[0].name!=null){
                html = ``
                for(let i=0; i<data.length;i++){
                    if(data[i].pokemon_id==null){
                        html += `
                        <div id ="recent">
                            <div class="d-flex col a">
                                <h4>${data[i].name}</h3>
                                <a href="/pokemon/friend/${data[i].id}" class='disappear'>
                                    <button class="disappear fourt">Friend Pokemon</button></a>
                                <div class ="view">
                                    <form onsubmit="event.preventDefault(); viewPoke(this);">
                                        <input type="hidden" id="id" name="id" value="${data[i].id}">
                                        <button>View</button>
                                    </form>
                                    <span class="disappear"> | </span>
                                    <a href="/pokemon/setfree/${data[i].id}" class='disappear'>
                                    <button class="disappear">Free</button></a>
                                </div>
                            </div>
                            <img src="${data[i].img}" alt=""></img>
                        </div>
                        `
                    }
                    else{
                        html += `
                        <div id ="recent">
                            <div class="d-flex col a">
                                <h4>${data[i].name}</h3>
                                    <button class="disappear fourt">Friends!</button></a>
                                <div class ="view">
                                    <form onsubmit="event.preventDefault(); viewPoke(this);">
                                        <input type="hidden" id="id" name="id" value="${data[i].id}">
                                        <button>View</button>
                                    </form>
                                    <span class="disappear"> | </span>
                                    <a href="/pokemon/setfree/${data[i].id}" class='disappear'>
                                    <button class="disappear">Free</button></a>
                                </div>
                            </div>
                            <img src="${data[i].img}" alt=""></img>
                        </div>
                        `
                    }
                }
                document.getElementById("display").innerHTML = html
            }
        })
        .catch(err => console.log(err))
    fetch("http://localhost:5000/pokemon/rivals")
        .then(res => res.json())
        .then(data => {
            rivals = `
            <h1 class="fourt">Rivals:</h1>
            <table class='table table-dark eight'>
                <tr>
                    <th>Trainer</th>
                    <th>Recent Friended Pokemon:</th>
                </tr>`
            for(let i=0; i<data.length;i++){
                rivals +=`
                <tr>
                    <td>${data[i].first_name}</td>
                    <td>${data[i].name}</td>
                </tr>
                `
            }
            rivals += "</table>"
            document.getElementById("rivals").innerHTML = rivals
        })
}

const registerUser = (e) => {
    var form = new FormData(e)
    fetch("http://localhost:5000/user/register", {method: "POST", body:form})
            .then(res => res.json())
            .then(data => console.log(data))
}

const viewPoke = (e) => {
    var form = new FormData(e)
    fetch("http://localhost:5000/pokemon/view", {method:"POST", body:form})
        .then(res => res.json())
        .then(data =>{
            data = data[0]
            console.log(data)
            if (data.isShiny) {
                html = `
                <div class="f name">
                    <h4>${data.name}:</h4><h6>${data.type}</h6>
                </div>
                <img src="${data.img}" alt="shiny pokemon"></img>
                `
            }
            else {
                html = `
                <div class="f name">
                    <h4>${data.name}:</h4><h6>${data.type}</h6>
                </div>
                <img src="${data.img}" alt="shiny pokemon"></img>
                `
            }
            document.getElementById('game').innerHTML = html;
            document.getElementById('input').innerHTML = `<div class="nintendo-logo-body">${data.ability}</div>`
        })
}

const checkPoke = (e) => {
    var form = new FormData(e)
    match = match.toLowerCase()
    if (match != pokeName && tries ==0){
        if (num <= 3){
            alert(`It's okay, you'll get ${pokeName} next time`)
        }
        else if(num > 3 && num < 7){
            alert(`${pokeName} is dying of laughter`)
        }
        else {
            alert(`${pokeName} is asking if you're even trying`)
        }
        tries = 3;
        location.reload();
    }
    else if (match != pokeName) {
        if(tries === 2){
            alert(`Two more tries before this Pokemon runs away!`)
        }
        if(tries === 1){
            alert(`So close! Let's do it again!`)
        }
        tries--
    }
    if (match == pokeName){
        alert(`Nice job! You got a ${pokeName}!`)
        score++;
        fetch("http://localhost:5000/pokemon/create", {method: "POST", body:form})
            .then(res => res.json())
            .then(data => getPoke())
        randPoke()
    }
}

function randPoke() {
    tries = 2
    num = (Math.floor(Math.random() * (11 - 1)))
    if (num == 1) {
        isShiny = true
    }
    else {
        isShiny = false
    }
    document.getElementById('input').innerHTML = `<input type="text" autocomplete="off" class="textbox f fourt" name="name" oninput="updateMatch(this)"></input>`
    let html = ``;
    rand = (Math.floor(Math.random() * (end - start - 1))) + start;
    fetch(`https://pokeapi.co/api/v2/pokemon/${rand}`)
        .then(resp => resp.json())
        .then(data => {
            document.getElementById('pokedex').value = rand;
            pokeName = data.species.name
            if (isShiny) {
                html = `
                <h4 class="f score">Score: ${score}</h4>
                <img src="${data.sprites.front_shiny}" alt="shiny pokemon"></img>
                `
                document.getElementById('img').value = data.sprites.front_shiny;
            }
            else {
                html = `
                <h4 class="f score">Score: ${score}</h4>
                <img src="${data.sprites.front_default}" alt="pokemon"></img>
                `
                document.getElementById('img').value = data.sprites.front_default;
            }
            document.getElementById('game').innerHTML = html;
            document.getElementById('isShiny').value = isShiny;
            if (data.types[1]){
                type = data.types[0].type.name + " / " + data.types[1].type.name
            }
            else{
                type = data.types[0].type.name
            }
            document.getElementById('type').value = type
            if (data.abilities[1]){
                if (num >= 6){
                    ability = data.abilities[0].ability.name
                }
                else{
                    ability = data.abilities[1].ability.name
                }
            }
            else ability = data.abilities[0].ability.name
            document.getElementById('ability').value = ability;
        })
        .catch(err => console.log(err))
}
