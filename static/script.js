// Path: static/script.js
const URL = "http://127.0.0.1:5000";

rollButton = document.getElementById("roll-button");
pokeContainer = document.getElementById("poke-container");

let catchButton;
let currentPokemon;

const pokeRoll = async () => {
  try {
    console.log("Fetching from URL:", URL + "/gacha");
    const res = await fetch(URL + "/gacha");

    if (res.status !== 200) {
      throw new Error("Error");
    }

    const data = await res.json();

    pokeDisplay(data);
    currentPokemon = data;
  } catch (error) {
    console.error(error);
  }
};

const pokeDisplay = async (pokeObject) => {
  console.log(pokeObject);
  pokeContainer.innerHTML = "";

  const pokeSpeciesElement = document.createElement("h2");
  pokeSpeciesElement.textContent = pokeObject.species;

  const pokeImageElement = document.createElement("img");
  pokeImageElement.src = pokeObject.image;

  const pokeTypeElement = document.createElement("h3");
  pokeTypeElement.textContent = "Type 1: " + pokeObject.type1;

  const pokeType2Element = document.createElement("h3");
  pokeType2Element.textContent = "Type 2: " + pokeObject.type2;

  const pokeType3Element = document.createElement("h3");
  pokeType3Element.textContent = "Type 3: " + pokeObject.type3;

  const pokeHeightElement = document.createElement("h3");
  pokeHeightElement.textContent =
    "Height: " + pokeObject.height + " decimeters";

  const pokeWeightElement = document.createElement("h3");
  pokeWeightElement.textContent =
    "Weight: " + pokeObject.weight + " hectograms";

  catchButton = document.createElement("button");
  catchButton.textContent = "Catch";
  catchButton.id = "catchButton";

  pokeContainer.append(pokeSpeciesElement, pokeImageElement, pokeTypeElement);
  pokeContainer.append(pokeType2Element, pokeType3Element);
  pokeContainer.append(pokeHeightElement, pokeWeightElement);
  pokeContainer.append(catchButton);
};

const sendCatchRequest = async (pokemon) => {
  try {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(pokemon),
    };

    console.log("Sending catch request:", requestOptions);

    const response = await fetch(URL + "/catch", requestOptions);

    if (response.status !== 200) {
      throw new Error("Error sending catch request");
    }

    const responseData = await response.json();

    console.log(responseData.message);
    console.log("Catch request successful");
  } catch (error) {
    console.error(error);
  }
};

rollButton.addEventListener("click", function (event) {
  event.preventDefault();
  pokeRoll();
});

document.addEventListener("click", function (event) {
  event.preventDefault();
  if (event.target.id === "catchButton") {
    sendCatchRequest(currentPokemon);
  }
});
