<script lang="ts">
  import { onMount } from 'svelte';

  let output = $state('Loading…');
  let errorMsg = $state('');
  let status = $state('');
  let limit = $state(100);
  let refreshBtn: HTMLButtonElement;
  let loading = $state(false);

  async function fetchReports() {
    errorMsg = '';
    output = 'Loading…';
    status = 'Fetching…';
    loading = true;

    const safeLimit = Math.max(1, Math.min(1000, limit || 100));

    try {
      const res = await fetch(`/api/v1/reports?limit=${safeLimit}`);
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `Request failed with ${res.status}`);
      }
      const data = await res.json();
      output = JSON.stringify(data, null, 2);
      status = `Loaded ${Array.isArray(data) ? data.length : 0} records`;
    } catch (err: any) {
      errorMsg = err.message || String(err);
      output = '';
      status = 'Error';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    fetchReports();
  });
</script>

<main>
  <h1>Violation Reports</h1>
  <p class="muted">This is a simple debug view that dumps all reports from the database.</p>

  <div class="controls">
    <label for="limit">Limit</label>
    <input id="limit" type="number" min="1" max="1000" bind:value={limit} />
    <button bind:this={refreshBtn} disabled={loading} onclick={fetchReports}>Refresh</button>
    <span class="muted">{status}</span>
  </div>

  <pre>{output}</pre>
  {#if errorMsg}
    <div class="error">{errorMsg}</div>
  {/if}

  <p><a href="/">Back to Home</a></p>
</main>

<style>
  main {
    max-width: 1100px;
    margin: 0 auto;
  }

  h1 {
    margin: 0 0 1rem;
    font-size: 1.8rem;
  }

  .muted {
    color: #555;
    margin-bottom: 1rem;
  }

  pre {
    background: #0b1021;
    color: #e6e6e6;
    padding: 1rem;
    border-radius: 8px;
    overflow: auto;
  }

  .controls {
    margin: 1rem 0;
    display: flex;
    gap: .5rem;
    align-items: center;
  }

  input[type="number"] {
    width: 100px;
    padding: .4rem .6rem;
  }

  button {
    padding: .5rem .8rem;
    background: #0b5fff;
    color: white;
    border: 0;
    border-radius: 6px;
    cursor: pointer;
  }

  button:disabled {
    opacity: .6;
    cursor: not-allowed;
  }

  .error {
    color: #b00020;
    margin-top: .5rem;
  }

  a {
    color: #0b5fff;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }
</style>
