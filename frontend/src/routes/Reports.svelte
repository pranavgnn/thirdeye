<script lang="ts">
  import { onMount } from "svelte";
  import Button from "@/components/ui/Button.svelte";
  import Table from "@/components/ui/Table.svelte";
  import TableHead from "@/components/ui/TableHead.svelte";
  import TableBody from "@/components/ui/TableBody.svelte";
  import TableRow from "@/components/ui/TableRow.svelte";
  import TableHeader from "@/components/ui/TableHeader.svelte";
  import TableCell from "@/components/ui/TableCell.svelte";
  import Dialog from "@/components/ui/Dialog.svelte";
  import DialogHeader from "@/components/ui/DialogHeader.svelte";
  import DialogTitle from "@/components/ui/DialogTitle.svelte";
  import DialogContent from "@/components/ui/DialogContent.svelte";
  import Badge from "@/components/ui/Badge.svelte";
  import {
    RefreshCw,
    ArrowLeft,
    AlertCircle,
    Database,
    Eye,
    Calendar,
    Hash,
    MapPin,
  } from "lucide-svelte";

  interface Report {
    id: number;
    reporter_phone: string;
    reported_timestamp: string;
    reported_image: string;
    license_plate: string;
    violations: Array<{
      name: string;
      category: string;
      fine_amount: number;
      section: string;
    }>;
    confidence_score: number;
    short_description: string;
    is_violation: boolean;
    title: string;
  }

  let reports = $state<Report[]>([]);
  let errorMsg = $state("");
  let status = $state("");
  let limit = $state(100);
  let loading = $state(false);
  let selectedReport = $state<Report | null>(null);
  let dialogOpen = $state(false);

  async function fetchReports() {
    errorMsg = "";
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
      reports = data;
      status = `Loaded ${reports.length} records`;
    } catch (err: any) {
      errorMsg = err.message || String(err);
      reports = [];
      status = "Error";
    } finally {
      loading = false;
    }
  }

  function viewReport(report: Report) {
    selectedReport = report;
    dialogOpen = true;
  }

  function formatDate(dateStr: string) {
    return new Date(dateStr).toLocaleString("en-IN", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  onMount(() => {
    fetchReports();
  });
</script>

<main class="min-h-screen py-16">
  <div class="container max-w-7xl mx-auto px-4">
    <div class="mb-8">
      <h1
        class="text-4xl font-bold tracking-tight mb-2 flex items-center gap-3"
      >
        <Database size={36} />
        Violation Reports
      </h1>
      <p class="text-muted-foreground">
        View and manage all traffic violation reports
      </p>
    </div>

    <div class="bg-card border rounded-2xl p-6 shadow-sm mb-6">
      <div class="flex items-center gap-4 mb-6">
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
          <span class="text-sm text-muted-foreground font-medium">{status}</span
          >
        {/if}
      </div>

      {#if errorMsg}
        <div
          class="bg-destructive/10 border-l-4 border-destructive p-4 rounded-lg mb-4"
        >
          <div class="flex items-start gap-3">
            <AlertCircle size={20} class="text-destructive shrink-0 mt-0.5" />
            <p class="text-sm text-destructive font-medium">{errorMsg}</p>
          </div>
        </div>
      {/if}

      {#if reports.length > 0}
        <div class="rounded-lg border">
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>ID</TableHeader>
                <TableHeader>Date & Time</TableHeader>
                <TableHeader>License Plate</TableHeader>
                <TableHeader>Violations</TableHeader>
                <TableHeader>Confidence</TableHeader>
                <TableHeader>Status</TableHeader>
                <TableHeader class="text-right">Actions</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {#each reports as report}
                <TableRow
                  class="cursor-pointer"
                  onclick={() => viewReport(report)}
                >
                  <TableCell class="font-mono text-xs">#{report.id}</TableCell>
                  <TableCell>
                    <div class="flex items-center gap-2">
                      <Calendar size={14} class="text-muted-foreground" />
                      <span class="text-sm"
                        >{formatDate(report.reported_timestamp)}</span
                      >
                    </div>
                  </TableCell>
                  <TableCell>
                    <div class="flex items-center gap-2">
                      <MapPin size={14} class="text-muted-foreground" />
                      <span class="font-mono font-semibold"
                        >{report.license_plate || "N/A"}</span
                      >
                    </div>
                  </TableCell>
                  <TableCell>
                    {#if report.violations && report.violations.length > 0}
                      <div class="flex flex-wrap gap-1">
                        {#each report.violations.slice(0, 2) as violation}
                          <Badge variant="destructive" class="text-xs"
                            >{violation.name}</Badge
                          >
                        {/each}
                        {#if report.violations.length > 2}
                          <Badge variant="secondary" class="text-xs"
                            >+{report.violations.length - 2}</Badge
                          >
                        {/if}
                      </div>
                    {:else}
                      <span class="text-muted-foreground text-sm">None</span>
                    {/if}
                  </TableCell>
                  <TableCell>
                    <div class="flex items-center gap-2">
                      <div
                        class="w-16 h-2 bg-muted rounded-full overflow-hidden"
                      >
                        <div
                          class="h-full transition-all {report.confidence_score >=
                          0.7
                            ? 'bg-green-500'
                            : 'bg-amber-500'}"
                          style="width: {report.confidence_score * 100}%"
                        ></div>
                      </div>
                      <span class="text-xs font-medium"
                        >{Math.round(report.confidence_score * 100)}%</span
                      >
                    </div>
                  </TableCell>
                  <TableCell>
                    {#if report.is_violation}
                      <Badge variant="destructive">Violation</Badge>
                    {:else}
                      <Badge variant="secondary">No Violation</Badge>
                    {/if}
                  </TableCell>
                  <TableCell class="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      onclick={() => viewReport(report)}
                    >
                      <Eye size={16} />
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              {/each}
            </TableBody>
          </Table>
        </div>
      {:else if !loading}
        <div class="text-center py-12">
          <Database size={48} class="mx-auto text-muted-foreground mb-4" />
          <p class="text-lg text-muted-foreground">No reports found</p>
        </div>
      {/if}
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

<Dialog bind:open={dialogOpen}>
  {#if selectedReport}
    <DialogHeader>
      <DialogTitle>{selectedReport.title || "Violation Report"}</DialogTitle>
    </DialogHeader>
    <DialogContent class="max-h-[70vh] overflow-y-auto">
      <div class="space-y-4">
        <div class="flex items-center gap-2 text-sm text-muted-foreground">
          <Hash size={14} />
          <span>Report ID: {selectedReport.id}</span>
        </div>

        {#if selectedReport.reported_image}
          <div class="rounded-lg overflow-hidden border">
            <img
              src={selectedReport.reported_image}
              alt="Violation Evidence"
              class="w-full h-auto"
            />
          </div>
        {/if}

        <div>
          <h4 class="font-semibold mb-2">License Plate</h4>
          <p class="font-mono text-lg">
            {selectedReport.license_plate || "Not detected"}
          </p>
        </div>

        <div>
          <h4 class="font-semibold mb-2">Description</h4>
          <p class="text-sm">
            {selectedReport.short_description || "No description available"}
          </p>
        </div>

        {#if selectedReport.violations && selectedReport.violations.length > 0}
          <div>
            <h4 class="font-semibold mb-2">Violations Detected</h4>
            <div class="space-y-2">
              {#each selectedReport.violations as violation}
                <div class="p-3 border rounded-lg">
                  <div class="flex items-start justify-between mb-1">
                    <span class="font-medium">{violation.name}</span>
                    <Badge variant="destructive">₹{violation.fine_amount}</Badge
                    >
                  </div>
                  <p class="text-xs text-muted-foreground">
                    Category: {violation.category}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    Section: {violation.section}
                  </p>
                </div>
              {/each}
            </div>
          </div>
        {/if}

        <div>
          <h4 class="font-semibold mb-2">Report Details</h4>
          <div class="space-y-1 text-sm">
            <div class="flex justify-between">
              <span class="text-muted-foreground">Reported:</span>
              <span>{formatDate(selectedReport.reported_timestamp)}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Confidence:</span>
              <span>{Math.round(selectedReport.confidence_score * 100)}%</span>
            </div>
            {#if selectedReport.reporter_phone}
              <div class="flex justify-between">
                <span class="text-muted-foreground">Reporter:</span>
                <span class="font-mono">{selectedReport.reporter_phone}</span>
              </div>
            {/if}
          </div>
        </div>
      </div>
    </DialogContent>
    <div class="mt-4 flex justify-end">
      <Button onclick={() => (dialogOpen = false)}>Close</Button>
    </div>
  {/if}
</Dialog>
