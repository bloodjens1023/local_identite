<script>
  // @ts-nocheck

  import { onMount } from "svelte";

  import { goto } from "$app/navigation";
  import Erreur from "../../../Components/Erreur.svelte";
  // import HeaderAttenteSuperAdmin from "../../../Components/HeaderAttenteSuperAdmin.svelte";

  // import StatPieAdmin from "../../../Components/StatPieAdmin.svelte";
  // import StatUser from "../../../Components/StatUser.svelte";
  // import FooterAttenteSuperAdmin from "../../../Components/FooterAttenteSuperAdmin.svelte";
  import Chargement from "../../../Components/Chargement.svelte";
  import HeaderAttenteAdmin from "../../../Components/HeaderAttenteAdmin.svelte";
  import FooterAttenteAdmin from "../../../Components/FooterAttenteAdmin.svelte";
  import Avatar from "../../../Components/Avatar.svelte";

  let loads = true;
  setTimeout(() => {
    loads = false;
  }, 1000);

  function filter(a) {
    return "http://localhost:8000/" + a;
  }
  let val = "";
  let post = [];
  let users = "";
  const getPosts = async () => {
    users = localStorage.getItem("chef");

    const res = await fetch("http://localhost:8000/afficheChef/" + users);

    const data = await res.json();
    const filter = data.data;

    return filter[0];
  };

  onMount(async () => {
    try {
      let id = localStorage.getItem("chef");

      if (id == null || id == undefined || id == "") {
        goto("/Error");
      }
      post = await getPosts();
    } catch (error) {
      goto("/Error");
    }
  });
</script>

<div>
  <HeaderAttenteAdmin men="active" />
  <br />
  <br />
  <br />
  {#await getPosts()}
    <center
      style="height: 400px; display: flex; align-items: center; justify-content: center;"
    >
      <Chargement />
    </center>
  {:then data}
    {#if users != undefined}
      <div style="padding: 0px 30px 0px 100px;">
        <h1>Vos informations</h1>
        <hr />
      </div>
      <br />
      <br />
      <div
        style="display: flex; align-items: center; justify-content: center; flex-direction: column;"
      >
        <div class="info">
          <center> <h2>Information Personnel</h2></center>
          <br /><br />
          <div class="prev">
            <center style="width: 30%; margin-bottom: 30px;">
              <a href="/SuperAdmin/MenuSuperAdmin"
                ><Avatar
                  width="100"
                  round={true}
                  userFullName="Admin"
                  src={filter(data["photo"])}
                /></a
              >
            </center>
            <div class="prop">
              <p>Nom : {data["nom"]}</p>
              <p>Prenom : {data["prenom"]}</p>
              <p>Email : {data["email"]}</p>
              <p>CNI : {data["cni"]}</p>
              <p>Tel : {data["tel"]}</p>
              <div style="display: flex;">
                <p style="">Mots de passe :</p>
                <p style="overflow: hidden; width: 300px;">
                  {data["password"]}
                </p>
              </div>
            </div>
          </div>
          <br />
          <div class="bones">
            <a
              href="/Chef/ModifAdmin"
              class="btn btn-dark"
              style="height:50px; width:200px; margin-right: 20px;">Modifier</a
            >
            <button
              class="btn btn-outline-danger"
              style="height:50px; width:200px; margin-right: 20px;"
              on:click={() => {
                localStorage.removeItem("chef");
                goto("/Chef/ConnexionAdmin");
              }}>Déconnecter</button
            >
          </div>
        </div>
        <br />
        <br />
        <br />
      </div>
    {:else}
      <Erreur />
    {/if}
  {/await}
  <br />
  <br />
  <br />
  <FooterAttenteAdmin />
</div>

<style>
  .prev {
    display: flex;
    justify-content: space-between;
  }
  h1 {
    font-size: 2rem;
    font-weight: bold;
  }
  p {
    font-size: 1.4em;
  }
  h2 {
    font-size: 1.7rem;
    font-weight: bold;
    text-decoration: underline;
  }
  .info {
    width: 90%;
    border: 3px solid black;
    border-radius: 3px 3px 20px 20px;
    padding: 30px 10px 40px 30px;
  }
  .photo {
    width: 200px;
    height: 200px;
    border: 1px solid black;
    padding: 20px;
    border-radius: 20px;
  }
  .prop {
    width: 70%;
  }
  .bones {
    display: flex;
    justify-content: right;
    padding: 20px;
  }

  @media only screen and (max-width: 768px) {
    p {
      font-size: 1em;
    }
    h1 {
      font-size: 1.7rem;
    }
    .prev {
      flex-direction: column;
      align-items: center;
    }
    .photo {
      margin-bottom: 30px;
    }
    .bones {
      justify-content: center;
    }
  }
</style>
