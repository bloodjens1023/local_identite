<script>
  // @ts-nocheck

  import Chart from "chart.js/auto";
  import { onMount } from "svelte";

  export let type = "doughnut";
  export let nom = "myChart";

  let anne;
  let dataa = [1, 1, 1];
  let datass = {
    labels: ["en cours", "refuser", "accepter"],
    datasets: [
      {
        label: "Statitique",
        data: dataa,
        backgroundColor: ["#FFA500", "#DC3545", "#28A745"],
      },
    ],
  };

  let ctx;
  let myChart;

  async function loadstat() {
    let id = anne;
    try {
      const response = await fetch(
        "http://localhost:8000/api_stat_arrondissement_tous/" + id
      );
      const data = await response.json();
      const co = data.data;
      creer([co[0]["encour"], co[0]["refuser"], co[0]["accepter"]]);
    } catch (error) {
      console.error("Erreur lors de la récupération des demandes:", error);
    }
  }
  let arrond = 1;
  let region = 1;
  let district = 1;

  let users = [];
  let filtrer = users;
  let arrondissements = [];
  let districts = [];
  let regions = [];
  let id = [];
  async function fetchArrondissements() {
    arrondissements = [];
    try {
      const response = await fetch(
        "http://localhost:8000/get_arrond_district/" + district
      );
      const data = await response.json();
      arrondissements = data.data;
      arrond = "";
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des arrondissements:",
        error
      );
    }
  }
  async function fetchregion() {
    arrondissements = [];

    try {
      const response = await fetch("http://localhost:8000/get_region/");
      const data = await response.json();
      regions = data.data;
      arrond = "";
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des arrondissements:",
        error
      );
    }
  }

  async function fetchDistrict() {
    districts = [];
    try {
      const response = await fetch(
        "http://localhost:8000/get_district/" + region
      );
      const data = await response.json();
      districts = data.data;
      arrond = "";
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des arrondissements:",
        error
      );
    }
  }
  onMount(async () => {
    fetchregion();
    ctx = document.getElementById(nom);
    myChart = new Chart(ctx, {
      type: type,
      data: datass,
      options: {
        scales: {},
      },
    });
  });

  function creer(data) {
    datass.datasets[0].data = data;
    myChart.update();
  }
</script>

<div class="resp">
  <canvas id={nom}></canvas>
  <br />
  <div class="regroup">
    <div>
      <select
        class="form-select"
        aria-label=" select example"
        on:change={(e) => {
          region = e.target.value;

          if (e.target.value != "Région") {
            fetchDistrict();
          } else {
            arrondissements = [];
            districts = [];
          }
        }}
      >
        <option selected>Région</option>

        {#each regions as user}
          <option value={user.id}>{user.nom}</option>
        {/each}
      </select>
    </div>
    <div>
      <select
        class="form-select"
        aria-label=" select example"
        on:change={(e) => {
          district = e.target.value;
          if (e.target.value != "District") {
            fetchArrondissements();
          } else {
            arrondissements = [];
          }
        }}
      >
        <option selected>District</option>

        {#each districts as user}
          <option value={user.id}>{user.nom}</option>
        {/each}
      </select>
    </div>
    <div>
      <select
        class="form-select"
        aria-label=" select example"
        on:change={(e) => {
          anne = e.target.value;
          loadstat();
        }}
      >
        <option selected>Arrondissement</option>

        {#each arrondissements as user}
          <option value={user.id}>{user.nom}</option>
        {/each}
      </select>
    </div>
    <br />
  </div>
</div>

<style>
  .regroup {
    display: flex;
    align-items: center;
    justify-content: center;

    gap: 10px;
  }
  select {
    max-width: 200px;
    width: 200px;
  }
  .resp {
    width: 300px;
  }
  @media only screen and (max-width: 1000px) {
    .regroup {
      flex-direction: column;
    }
    select {
      max-width: 250px;
      width: 250px;
    }
    .resp {
      width: 250px;
    }
  }
</style>
