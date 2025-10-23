<script lang="ts">
  import { onMount } from "svelte";
  import Card from "@/components/ui/Card.svelte";
  import CardHeader from "@/components/ui/CardHeader.svelte";
  import CardTitle from "@/components/ui/CardTitle.svelte";
  import CardDescription from "@/components/ui/CardDescription.svelte";
  import CardContent from "@/components/ui/CardContent.svelte";
  import Button from "@/components/ui/Button.svelte";
  import Alert from "@/components/ui/Alert.svelte";
  import AlertDescription from "@/components/ui/AlertDescription.svelte";

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

<main class="min-h-screen bg-linear-to-b from-background to-secondary/20 py-16">
  <div class="container max-w-5xl mx-auto px-4">
    <div class="mb-8">
      <h1 class="text-4xl font-bold tracking-tight mb-2">Violation Reports</h1>
      <p class="text-muted-foreground">
        Debug view of all violation reports from the database.
      </p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Report Data</CardTitle>
        <CardDescription>Fetched from /api/v1/reports endpoint</CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="flex items-center gap-3">
          <label for="limit" class="text-sm font-medium">Limit</label>
          <input
            id="limit"
            type="number"
            min="1"
            max="1000"
            bind:value={limit}
            class="w-24 h-10 rounded-xl border border-input bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          <Button onclick={fetchReports} disabled={loading}>
            {loading ? "Refreshing..." : "Refresh"}
          </Button>
          {#if status}
            <span class="text-sm text-muted-foreground">{status}</span>
          {/if}
        </div>

        {#if errorMsg}
          <Alert
            class="border-destructive bg-destructive/10 dark:bg-destructive/20"
          >
            <AlertDescription class="text-destructive">
              {errorMsg}
            </AlertDescription>
          </Alert>
        {/if}

        <pre
          class="p-4 rounded-xl bg-slate-950 dark:bg-slate-900 text-slate-50 text-sm overflow-auto max-h-[600px] border border-slate-800">{output}</pre>
      </CardContent>
    </Card>

    <div class="mt-8 text-center">
      <a href="/" class="text-sm font-medium text-primary hover:underline">
        ← Back to Home
      </a>
    </div>
  </div>
</main>
