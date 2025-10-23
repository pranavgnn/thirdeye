<script lang="ts">
  import { onMount } from "svelte";
  import Button from "@/components/ui/Button.svelte";
  import { RefreshCw, ArrowLeft, AlertCircle, Database } from "lucide-svelte";

  let output = $state("Loading…");
  let errorMsg = $state("");
  let status = $state("");
  let limit = $state(100);
  let loading = $state(false);

  async function fetchReports() {
    errorMsg = "";
    output = "Loading…";
    status = "Fetching…";
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
      output = "";
      status = "Error";
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    fetchReports();
  });
</script>

<main class="min-h-screen py-16">
  <div class="container max-w-6xl mx-auto px-4">
    <div class="mb-8">
      <h1 class="text-4xl font-bold tracking-tight mb-2 flex items-center gap-3">
        <Database size={36} />
        Violation Reports
      </h1>
      <p class="text-muted-foreground">
        Debug view of all violation reports from the database
      </p>
    </div>

    <div class="bg-card border rounded-2xl p-6 shadow-sm mb-6">
      <div class="flex items-center gap-4 mb-4">
        <label for="limit" class="text-sm font-semibold">Records Limit:</label>
        <input
          id="limit"
          type="number"
          min="1"
          max="1000"
          bind:value={limit}
          class="w-32 h-11 rounded-lg border-2 border-input bg-transparent px-4 py-2 text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:border-primary"
        />
        <Button onclick={fetchReports} disabled={loading}>
          <RefreshCw size={18} class={loading ? "animate-spin" : ""} />
          {loading ? "Refreshing..." : "Refresh Data"}
        </Button>
        {#if status}
          <span class="text-sm text-muted-foreground font-medium">{status}</span>
        {/if}
      </div>

      {#if errorMsg}
        <div class="bg-destructive/10 border-l-4 border-destructive p-4 rounded-lg mb-4">
          <div class="flex items-start gap-3">
            <AlertCircle size={20} class="text-destructive shrink-0 mt-0.5" />
            <p class="text-sm text-destructive font-medium">{errorMsg}</p>
          </div>
        </div>
      {/if}

      <div class="rounded-xl border-2 overflow-hidden">
        <pre class="p-6 bg-slate-950 dark:bg-slate-900 text-slate-50 text-sm overflow-auto max-h-[600px] font-mono">{output}</pre>
      </div>
    </div>

    <div class="text-center">
      <a href="/">
        <Button variant="outline">
          <ArrowLeft size={18} />
          Back to Home
        </Button>
      </a>
    </div>
  </div>
</main>
