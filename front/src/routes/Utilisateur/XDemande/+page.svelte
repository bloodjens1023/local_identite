<script>
  // @ts-nocheck

  import HeaderAttente from "../../../Components/HeaderAttente.svelte";
  import DupliUse from "../../../Components/DupliUse.svelte";
  import DupliPerte from "../../../Components/DupliPerte.svelte";
  import Prima from "../../../Components/Prima.svelte";
  import Erreur from "../../../Components/Erreur.svelte";

  import { onMount } from "svelte";
  import { Motion } from "svelte-motion";
  import FooterAttenteUtilisateur from "../../../Components/FooterAttenteUtilisateur.svelte";
  import { goto } from "$app/navigation";
  import Chargement from "../../../Components/Chargement.svelte";
  import ResultatDemande from "../../../Components/ResultatDemande.svelte";
  import toast, { Toaster } from "svelte-french-toast";

  $: post = {
    nom: "",
    prenom: "",
    adresse: "",
    numCni: "",
    photo: "",
    certificate: "",
    declarationPerte: "",
    acteNaissance: "",
    etatDocument: "",
    typeDocument: "",
  };

  let users = "";
  const getPosts = async () => {
    try {
      users = sessionStorage.getItem("identifiant");

      if (users == null || users == undefined || users == "") {
        goto("/Error");
      }
      const res = await fetch("http://localhost:8000/afficheDocument/" + users);

      const data = await res.json();

      post = data;
      console.log(data);
    } catch (error) {
      toast.error("Erreur de serveur", {
        style: "font-size:15px; padding:10px",
        duration: 2000,
      });
    }
  };

  onMount(async () => {
    post = getPosts();
  });
</script>

<Toaster />
<div>
  <HeaderAttente dem="active" />

  {#await getPosts()}
    <Chargement />
  {:then dons}
    {#if users == undefined}
      <Erreur />
    {:else}
      <br /><br /><br />
      {#if post["archiver"] == false}
        {#if post["etatDocument"] == "encours"}
          {#if post["typeDocument"] == "duplicatatUse"}
            <DupliUse donne={post} user={users} />
            <br /><br /><br /><br /><br />
          {/if}
          {#if post["typeDocument"] == "duplicatatPerte"}
            <DupliPerte donne={post} user={users} />
            <br /><br /><br /><br /><br />
          {/if}

          {#if post["typeDocument"] == "primata"}
            <Prima donne={post} user={users} />
            <br /><br /><br /><br /><br />
          {/if}
        {/if}
        {#if post["etatDocument"] == "accepter"}
          <ResultatDemande donne={post} resultat={"accepter"} user={users} />
        {/if}
        {#if post["etatDocument"] == "refuser"}
          <ResultatDemande donne={post} resultat="refuser" user={users} />
        {/if}
        {#if post["donne"] == "aucun"}
          <center
            style="height: 70vh; display: flex; align-items: center; justify-content: center; flex-direction: column; gap:30px"
          >
            <div class="loader"></div>
            <div class="load"><h1>Aucun demande identifier</h1></div>
            <br />
            <Motion
              let:motion
              whileHover={{ scale: 1.2 }}
              whileTap={{ scale: 1.1 }}
            >
              <a class="btn btn-success" href="/Utilisateur/Step" use:motion
                >envoyer un demande</a
              >
            </Motion>
          </center>
        {/if}
      {/if}
      {#if post["archiver"] == true}
        <center
          style="height: 70vh; display: flex; align-items: center; justify-content: center; flex-direction: column; gap:30px"
        >
          <div class="loaders"></div>
          <div class="load"><h1>Envoie de demande indisponible</h1></div>

          <br />
        </center>
      {/if}
    {/if}
  {/await}

  <FooterAttenteUtilisateur />
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Reddit+Mono:wght@200..900&display=swap");
  * {
    font-family: "Poppins";
  }
  .loader {
    width: fit-content;
    font-weight: bold;
    font-family: monospace;
    font-size: 30px;
    background: radial-gradient(circle closest-side, #000 94%, #0000)
      right/calc(200% - 1em) 100%;
    animation: l24 3s infinite alternate linear;
  }

  .loader::before {
    content: "Aucun Demande identifier";
    line-height: 1em;
    color: #0000;
    background: inherit;
    background-image: radial-gradient(circle closest-side, #fff 94%, #000);
    -webkit-background-clip: text;
    background-clip: text;
  }
  .loaders {
    width: fit-content;
    font-weight: bold;
    font-family: monospace;
    font-size: 30px;
    background: radial-gradient(circle closest-side, #000 94%, #0000)
      right/calc(200% - 1em) 100%;
    animation: l24 3s infinite alternate linear;
  }

  .loaders::before {
    content: "Envoie de demande indisponible";
    line-height: 1em;
    color: #0000;
    background: inherit;
    background-image: radial-gradient(circle closest-side, #fff 94%, #000);
    -webkit-background-clip: text;
    background-clip: text;
  }
  .load {
    display: none;
  }

  @keyframes l24 {
    100% {
      background-position: left;
    }
  }

  @media only screen and (max-width: 768px) {
    .loader {
      display: none;
    }
    .loaders {
      display: none;
    }
    .load {
      display: block;
    }
  }
</style>
