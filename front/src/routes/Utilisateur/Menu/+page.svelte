<script>
  // @ts-nocheck
  import HeaderAttente from "../../../Components/HeaderAttente.svelte";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import Erreur from "../../../Components/Erreur.svelte";
  import FooterAttenteUtilisateur from "../../../Components/FooterAttenteUtilisateur.svelte";
  import Chargement from "../../../Components/Chargement.svelte";
  import Rate from "../../../Components/Rate.svelte";
  import Avatar from "../../../Components/Avatar.svelte";

  function filter(a) {
    console.log("http://localhost:8000/" + a);
    return "http://localhost:8000/" + a;
  }

  let val = "";
  let post = [];
  let users = "";
  const getPosts = async () => {
    users = localStorage.getItem("identifiant");

    const res = await fetch(
      "http://localhost:8000/afficheUtilisateur/" + users
    );

    const data = await res.json();
    const filter = data;

    // let r = filter.split("/");
    // r.shift();
    // let z = r.join("/");

    return filter;
  };

  onMount(async () => {
    try {
      let id = localStorage.getItem("identifiant");

      if (id == null || id == undefined || id == "") {
        goto("/Error");
      } else {
        post = await getPosts();
      }
    } catch (error) {
      goto("/Error");
    }
  });
</script>

<div>
  {#await getPosts()}
    <HeaderAttente men="active" />
    <br />
    <br />
    <br />

    <center
      style="height: 400px; display: flex; align-items: center; justify-content: center;"
    >
      <Chargement />
    </center>
    <FooterAttenteUtilisateur />
  {:then data}
    {#if users != undefined}
      <HeaderAttente men="active" />
      <br />
      <br />
      <br />
      <div style="display: flex; align-items: center; justify-content: center;">
        <p style="font-size:2.3em; font-weight: bold;">Vos informations</p>
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
              {#if data["photo"] != ""}
                <a href="/SuperAdmin/MenuSuperAdmin"
                  ><Avatar
                    width="200"
                    round={true}
                    userFullName={users}
                    src={filter(data["photo"])}
                  /></a
                >
              {/if}
              {#if data["photo"] == ""}
                <a href="/SuperAdmin/MenuSuperAdmin"
                  ><Avatar width="200" round={true} userFullName={users} /></a
                >
              {/if}
            </center>
            <div class="prop">
              <p>Identifiant : {data["identifiant"]}</p>
              <p>Email : {data["email"]}</p>
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
              href="/Utilisateur/Update"
              class="btn btn-dark"
              style="height:50px; width:200px; margin-right: 20px;">Modifier</a
            >
            <button
              class="btn btn-outline-danger"
              style="height:50px; width:200px; margin-right: 20px;"
              on:click={() => {
                localStorage.removeItem("identifiant");
                localStorage.removeItem("premier");
                goto("/Utilisateur/Connexion");
              }}>Déconnecter</button
            >
          </div>
        </div>
        <br />
        <br />
        <br />
        <div class="rate">
          <Rate simple={true} />
        </div>
        <br />
        <br />
        <br />
      </div>
      <FooterAttenteUtilisateur />
    {:else}
      <Erreur />
    {/if}
  {/await}
</div>

<style>
  .prev {
    display: flex;
    justify-content: space-between;
  }
  .rate {
    width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
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
    .rate {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .prev {
      flex-direction: column;
      align-items: center;
    }

    .bones {
      justify-content: center;
    }
  }
</style>
