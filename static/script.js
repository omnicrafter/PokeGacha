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
  pokeContainer.classList.add("card", "mt-4", "border", "border-dark", "p-4");

  const pokeSpeciesElement = document.createElement("h2");
  pokeSpeciesElement.textContent = capitalizeFirst(pokeObject.species);
  pokeSpeciesElement.classList.add("card-title", "text-center");

  const pokeImageElement = document.createElement("img");
  pokeImageElement.src = pokeObject.image;

  const pokeTypeElement = document.createElement("h3");
  if (pokeObject.type2 === "Unknown") {
    pokeTypeElement.textContent = "Type: " + capitalizeFirst(pokeObject.type1);
  } else if (pokeObject.type3 === "Unknown") {
    pokeTypeElement.textContent =
      "Type: " +
      capitalizeFirst(pokeObject.type1) +
      ", " +
      capitalizeFirst(pokeObject.type2);
  } else {
    pokeTypeElement.textContent =
      "Type: " +
      capitalizeFirst(pokeObject.type1) +
      ", " +
      capitalizeFirst(pokeObject.type2) +
      ", " +
      capitalizeFirst(pokeObject.type3);
  }

  const pokeHeightElement = document.createElement("h3");
  pokeHeightElement.textContent =
    "Height: " + pokeObject.height + " Decimeters";

  const pokeWeightElement = document.createElement("h3");
  pokeWeightElement.textContent =
    "Weight: " + pokeObject.weight + " Hectograms";

  catchButton = document.createElement("button");
  catchButton.textContent = "Catch";
  catchButton.id = "catchButton";
  catchButton.classList.add("btn", "btn-success");

  catchButton.addEventListener("click", function () {
    console.log("Catch button clicked");
    sendCatchRequest(pokeObject);
  });

  pokeContainer.append(pokeSpeciesElement, pokeImageElement, pokeTypeElement);
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
    pokeContainer.innerHTML =
      "Successfully caught " + capitalizeFirst(pokemon.species) + "!";
  } catch (error) {
    console.error(error);
  }
};

rollButton.addEventListener("click", function (event) {
  event.preventDefault();
  pokeRoll();
});

const capitalizeFirst = (word) => {
  const capitalizedFirst = word.charAt(0).toUpperCase();
  const restOfWord = word.slice(1).toLowerCase();
  return capitalizedFirst + restOfWord;
};
