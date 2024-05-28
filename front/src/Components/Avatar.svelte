<script>
  // @ts-nocheck

  export let userFullName;
  export let avatarColors = [
    "#1abc9c",
    "#2ecc71",
    "#3498db",
    "#9b59b6",
    "#34495e",
    "#16a085",
    "#27ae60",
    "#2980b9",
    "#8e44ad",
    "#2c3e50",
    "#f1c40f",
    "#e67e22",
    "#e74c3c",
    "#ecf0f1",
    "#95a5a6",
    "#f39c12",
    "#d35400",
    "#c0392b",
    "#bdc3c7",
    "#7f8c8d",
  ];
  import { onMount } from "svelte";
  export let width = 32;
  export let height = width;
  export let round = true;
  export let src = "";
  let avatarImage = "";

  function LetterAvatar(name, size) {
    name = name || "";
    size = size || 60;

    var colours = avatarColors,
      nameSplit = String(name).toUpperCase().split(" "),
      initials,
      charIndex,
      colourIndex,
      canvas,
      context,
      dataURI;

    if (nameSplit.length == 1) {
      initials = nameSplit[0] ? nameSplit[0].charAt(0) : "?";
    } else {
      initials = nameSplit[0].charAt(0) + nameSplit[1].charAt(0);
    }

    if (window.devicePixelRatio) {
      size = size * window.devicePixelRatio;
    }

    charIndex = (initials == "?" ? 72 : initials.charCodeAt(0)) - 64;
    colourIndex = charIndex % 20;
    canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;
    context = canvas.getContext("2d");

    // @ts-ignore
    context.fillStyle = colours[colourIndex - 1];
    // @ts-ignore
    context.fillRect(0, 0, canvas.width, canvas.height);
    // @ts-ignore
    context.font = Math.round(canvas.width / 2) + "px Arial";
    // @ts-ignore
    context.textAlign = "center";
    // @ts-ignore
    context.fillStyle = "#FFF";
    // @ts-ignore
    context.fillText(initials, size / 2, size / 1.5);

    dataURI = canvas.toDataURL();
    canvas = null;

    return dataURI;
  }

  onMount(() => {
    // @ts-ignore
    avatarImage.src = src !== "" ? src : LetterAvatar(userFullName, width);
  });
</script>

<img bind:this={avatarImage} class:round {width} {height} alt={userFullName} />

<style>
  .round {
    border-radius: 50%;
  }
  img {
    display: block; /* Makes the image a block element */
    margin: auto; /* Centers the image horizontally */
    border-radius: 50%; /* Makes the image round if it is set to be round */
  }
</style>
