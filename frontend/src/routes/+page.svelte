<script>
  export let data;
</script>

<h2>HOME</h2>

{#each data.measurements as foo}
  <li>pigeon: {foo.pigeon}</li>
{/each}
