<script>
  // @ts-nocheck

  import { onDestroy, onMount } from "svelte";
  import Card from "../../../Components/Card.svelte";
  import HeaderAttente from "../../../Components/HeaderAttente.svelte";
  import FooterAttenteUtilisateur from "../../../Components/FooterAttenteUtilisateur.svelte";
  import { goto } from "$app/navigation";
  import Chargement from "../../../Components/Chargement.svelte";
  import toast, { Toaster } from "svelte-french-toast";

  let users = [];
  let id = "";
  let filtrer = users;

  async function fetchUtilisateur() {
    try {
      const response = await fetch("http://localhost:8000/api_affiche_pub/");
      const data = await response.json();
      users = data.data; // Supposons que 'data' est le nom de la clé qui contient les Utilidateur dans la réponse JSON
      filtrer = users;
      console.log(filtrer);
    } catch (error) {
      console.error("Erreur lors de la récupération des Utilisateurs:", error);
    }
  }

  setInterval(() => {
    fetchUtilisateur();
  }, 100);

  function filter(a) {
    return "http://localhost:8000/" + a;
  }
  onMount(() => {
    try {
      id = sessionStorage.getItem("identifiant");

      if (id == null || id == undefined || id == "") {
        goto("/Error");
      } else {
        window.scrollTo({
          top: 0,
          behavior: "smooth", // Pour un défilement en douceur
        });
        fetchUtilisateur();
      }
    } catch (error) {
      goto("/Error");
    }
  });
</script>

<Toaster />
<div style="width: 100%; background-color: #e9ebee;">
  <HeaderAttente acc="active" />
  <br /><br /><br />
  <div style="background-color: #e9ebee;">
    {#each filtrer as user}
      <Card
        description={user["description"]}
        aimer={user["aimer"]}
        image={filter(user["photo"])}
        ids={user["id"]}
        detail={false}
      />
      <br /><br /><br />
    {/each}
    {#if filtrer.length == 0}
      <div
        style="height: 50vh; display: flex; align-items: center; justify-content: center;"
      >
        <!-- <Chargement /> -->
        <h1>Aucun publication</h1>
      </div>
    {/if}
  </div>
  <br /><br /><br /><br /><br />
  <FooterAttenteUtilisateur />
</div>
