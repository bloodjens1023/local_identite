<script>
  // @ts-nocheck
  import { onMount } from "svelte";
  import { Motion } from "svelte-motion";
  import ChargementConnect from "./ChargementConnect.svelte";
  import toast, { Toaster } from "svelte-french-toast";
  import Modal from "./Modal.svelte";
  import Accepter from "./Accepter.svelte";
  import Ers from "./Ers.svelte";
  import Spinner from "./Spinner.svelte";

  let donne = {};

  let showModal = false;
  let accepter_photo = false;
  let accepter_certif = false;

  let refuser_photo = false;
  let refuser_certif = false;

  let chargement_photo = true;
  let chargement_certif = true;

  let success = false;
  let error = false;
  let loads = false;
  export let onSubmit = () => {};
  export let update = false;

  const handleSubmit = async (event) => {
    event.preventDefault();
    let formdata = new FormData();
    formdata.append("type", "duplicatatUse");
    formdata.append("nom", donne.nom);
    formdata.append("prenom", donne.prenom);
    formdata.append("genre", donne.genre);
    formdata.append("numCni", donne.num);
    formdata.append("adresse", donne.adresse);
    formdata.append("photo", donne.photo);
    formdata.append("certificat", donne.resid);
    formdata.append("identifiant", localStorage.getItem("identifiant"));
    loads = true;
    let response;
    if (update) {
      let use = localStorage.getItem("identifiant");
      response = await fetch("http://localhost:8000/updateDocument/" + use, {
        method: "POST",
        body: formdata,
      });
    } else {
      response = await fetch("http://localhost:8000/api_demande/", {
        method: "POST",
        body: formdata,
      });
    }

    const data = await response.json();
    const message = data.message;
    console.log(message);

    if (message) {
      loads = false;
      toast.success("Document envoyé", {
        style: "font-size:15px; padding:10px",
        duration: 2000,
      });
      onSubmit(donne);
    } else {
      toast.error("Erreur de remplissage", {
        style: "font-size:15px; padding:10px",
        duration: 2000,
      });
      loads = false;
    }
  };

  let users = "";
  const getPosts = async () => {
    users = localStorage.getItem("identifiant");

    const res = await fetch("http://localhost:8000/afficheDocument/" + users);

    const data = await res.json();
    const filter = data;

    // let r = filter.split("/");
    // r.shift();
    // let z = r.join("/");

    return filter;
  };

  onMount(async () => {
    // @ts-ignore
    if (update) {
      let post = await getPosts();
      console.log(post);
      donne.nom = post["nom"];
      donne.prenom = post["prenom"];
      donne.adresse = post["adresse"];
      donne.num = post["numCni"];
    }
  });

  async function verifier_numero_CNI() {
    let formdata = new FormData();
    if (donne.num == undefined) {
      donne.num = "";
    }
    formdata.append("numCni", donne.num);
    let response = await fetch(
      "http://localhost:8000/verification_duplication/",
      {
        method: "POST",
        body: formdata,
      }
    );
    const data = await response.json();
    let users = data.data;
    console.log(donne.num);
    console.log(users);
    if (users === 0) {
      return 0;
    } else {
      return 1;
    }
  }

  async function verifier_document() {
    chargement_photo = true;
    chargement_certif = true;
    accepter_photo = false;

    accepter_certif = false;
    refuser_photo = false;
    refuser_certif = false;

    if (donne.num == "") {
      toast.error("Remplissez les champs ", {
        style: "font-size:15px; padding:10px",
        duration: 2000,
      });
    } else {
      if ((await verifier_numero_CNI()) === 1) {
        showModal = true;
        verif_photo();
        verif_certificat();
      } else {
        toast.error("Votre CNI n'est pas disponible dans nos base de données", {
          style: "font-size:15px; padding:10px",
          duration: 2000,
        });
      }
    }
  }

  const verif_certificat = async (event) => {
    try {
      let formdata = new FormData();
      formdata.append("certificat", donne.resid);
      let response;
      response = await fetch("http://localhost:8000/api_verif_certificat/", {
        method: "POST",
        body: formdata,
      });
      const data = await response.json();
      let users = data.data;
      if (users) {
        accepter_certif = true;
        chargement_certif = false;
      } else {
        refuser_certif = true;
        chargement_certif = false;
      }
    } catch (error) {
      showModal = false;
      toast.error("Erreur de serveur", {
        style: "font-size:15px; padding:10px",
        duration: 2000,
      });
    }
  };
  const verif_photo = async (event) => {
    try {
      let formdata = new FormData();
      formdata.append("photo", donne.photo);
      let response;
      response = await fetch("http://localhost:8000/api_verif_photo/", {
        method: "POST",
        body: formdata,
      });
      const data = await response.json();
      let users = data.data;
      if (users) {
        accepter_photo = true;
        chargement_photo = false;
        if (data.genre == "male") {
          donne.genre = 1;
        } else {
          donne.genre = 2;
        }
      } else {
        refuser_photo = true;
        chargement_photo = false;
      }
    } catch (error) {
      showModal = false;
      toast.error("Erreur de serveur", {
        style: "font-size:15px; padding:10px",
        duration: 2000,
      });
    }
  };
</script>

<Modal bind:showModal>
  <h2 style="margin: 30px; margin-right: 30px;">
    <small>Verification des informations</small>
  </h2>

  <ol
    class="definition-list"
    style="display: flex;
  flex-direction: column;
  align-items: baseline; width: 100%; padding:initial;"
  >
    <br />
    <div style="display: flex; gap: 30px;">
      {#if accepter_photo}
        <Accepter />
      {/if}
      {#if refuser_photo}
        <Ers />
      {/if}
      {#if chargement_photo}
        <Spinner />
      {/if}
      <p style="font-size: 1.1em;">Verification du photo d'identité</p>
    </div>
    <br />
    <div
      style="display: flex; gap: 30px; align-items: center; justify-content: center;  padding-left: 30px;"
    >
      {#if accepter_certif}
        <Accepter />
      {/if}
      {#if refuser_certif}
        <Ers />
      {/if}
      {#if chargement_certif}
        <Spinner />
      {/if}
      <div style="font-size: 1.1em;">
        Verification du certificat de résidence
      </div>
    </div>
    <br />
    <div
      style="width: 100%; display: flex; align-items: center; justify-content: center; padding-left: 30px;"
    >
      {#if !loads}
        {#if accepter_certif && accepter_photo}
          <input
            type="button"
            value="Suivant"
            class="btn btn-outline-dark"
            style="width: 300px;"
            on:click={handleSubmit}
          />
        {/if}
      {/if}

      {#if loads}
        <ChargementConnect />
      {/if}
    </div>
  </ol>
  <br /><br />
</Modal>
<Toaster />
<center>
  <form>
    <div class="forms">
      <div class="input-container">
        <input
          required
          id="input"
          type="text"
          bind:value={donne.nom}
          on:change={(e) => {
            donne.nom = e.target.value;
          }}
        />
        <label class="label" for="input">nom</label>
        <div class="underline"></div>
      </div>
      <div class="input-container">
        <input
          required
          id="input"
          type="text"
          bind:value={donne.prenom}
          on:change={(e) => {
            donne.prenom = e.target.value;
          }}
        />
        <label class="label" for="input">prenom</label>
        <div class="underline"></div>
      </div>
      <div class="input-container">
        <input
          required
          id="input"
          type="text"
          bind:value={donne.adresse}
          on:change={(e) => {
            donne.adresse = e.target.value;
          }}
        />
        <label class="label" for="input">adresse</label>
        <div class="underline"></div>
      </div>

      <div class="input-container">
        <input
          required
          id="input"
          type="text"
          bind:value={donne.num}
          on:change={(e) => {
            donne.num = e.target.value;
          }}
        />
        <label class="label" for="input">Numero CNI</label>
        <div class="underline"></div>
      </div>

      <div class="input-container form-control-lg">
        <div class="mb-5">
          <label for="formFile" class="form-label">Photos d'identité</label>
          <input
            class="form-control"
            type="file"
            required
            accept="image/* "
            id="formFile"
            bind:value={donne.photo}
            on:change={(e) => {
              donne.photo = e.target.files[0];
            }}
          />
        </div>

        <div class="mb-5">
          <label for="formFile" class="form-label"
            >Cértificat de résidence</label
          >
          <input
            class="form-control"
            type="file"
            required
            id="formFile"
            accept="image/* "
            bind:value={donne.resid}
            on:change={(e) => {
              donne.resid = e.target.files[0];
            }}
          />
        </div>

        <div class="input-container">
          {#if loads}
            <ChargementConnect />
          {/if}
        </div>
      </div>
    </div>
    {#if !loads}
      <div class="input-container">
        <Motion let:motion whileHover={{ rotate: "3deg" }}>
          <input
            type="button"
            value="Vérifier"
            class="button"
            use:motion
            on:click={verifier_document}
          />
        </Motion>
      </div>
    {/if}
  </form>
</center>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Reddit+Mono:wght@200..900&display=swap");

  * {
    font-family: "Poppins", "Helvetica";
  }
  .input-container {
    position: relative;
    margin: 50px auto;
    width: 350px;
  }

  .input-container input[type="text"] {
    font-size: 20px;
    width: 100%;
    border: none;
    border-bottom: 2px solid #000000;
    padding: 5px 0;
    background-color: transparent;
    outline: none;
  }

  .input-container .label {
    position: absolute;
    top: 0;
    left: 0;
    color: #000000;
    transition: all 0.3s ease;
    pointer-events: none;
  }

  .input-container input[type="text"]:focus ~ .label,
  .input-container input[type="text"]:valid ~ .label {
    top: -20px;
    font-size: 16px;
    font-weight: bold;
    color: #333;
  }

  .input-container .underline {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 2px;
    width: 100%;
    background-color: #333;
    transform: scaleX(0);
    transition: all 0.3s ease;
  }

  .input-container input[type="text"]:focus ~ .underline,
  .input-container input[type="text"]:valid ~ .underline {
    transform: scaleX(1);
  }
  .button {
    width: 100%;
    height: auto;
    padding: 10px 0;
    font-size: 1.3em;
    font-weight: bold;
    background-color: white;
    border: 4px solid #5f6468;
    color: #5f6468;
    border-radius: 3px 20px 20px 3px;
    transition: 0.2s all;
  }
  .button:hover {
    background-color: #5f6468;
    color: white;
  }
</style>
