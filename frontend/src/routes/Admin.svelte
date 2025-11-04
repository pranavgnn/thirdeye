<script lang="ts">
  import Button from "@/components/ui/Button.svelte";
  import Card from "@/components/ui/Card.svelte";
  import CardHeader from "@/components/ui/CardHeader.svelte";
  import CardTitle from "@/components/ui/CardTitle.svelte";
  import CardContent from "@/components/ui/CardContent.svelte";
  import Alert from "@/components/ui/Alert.svelte";
  import AlertDescription from "@/components/ui/AlertDescription.svelte";
  import Badge from "@/components/ui/Badge.svelte";
  import Table from "@/components/ui/Table.svelte";
  import TableHeader from "@/components/ui/TableHeader.svelte";
  import TableBody from "@/components/ui/TableBody.svelte";
  import TableRow from "@/components/ui/TableRow.svelte";
  import TableHead from "@/components/ui/TableHead.svelte";
  import TableCell from "@/components/ui/TableCell.svelte";
  import Dialog from "@/components/ui/Dialog.svelte";
  import DialogContent from "@/components/ui/DialogContent.svelte";
  import DialogHeader from "@/components/ui/DialogHeader.svelte";
  import DialogTitle from "@/components/ui/DialogTitle.svelte";
  import { 
    Shield, 
    LogOut, 
    RefreshCw, 
    AlertCircle, 
    CheckCircle,
    Eye,
    Flag,
    Filter,
    TrendingUp,
    FileText,
    AlertTriangle,
    Check,
    X,
    Clock
  } from "lucide-svelte";

  let isAuthenticated = $state(false);
  let password = $state("");
  let loginError = $state<string | null>(null);
  let isLoggingIn = $state(false);
  let authToken = $state<string | null>(null);

  let reports = $state<any[]>([]);
  let stats = $state<any>(null);
  let isLoadingReports = $state(false);
  let isLoadingStats = $state(false);
  let errorMsg = $state<string | null>(null);

  let filterFlaggedOnly = $state(false);
  let filterHasViolations = $state<boolean | null>(null);
  let filterPendingApproval = $state(false);

  let selectedReport = $state<any>(null);
  let showDetailDialog = $state(false);

  async function handleLogin() {
    if (!password) {
      loginError = "Please enter password";
      return;
    }
    
    isLoggingIn = true;
    loginError = null;

    try {
      const res = await fetch("/api/v1/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Login failed");
      }

      authToken = data.token;
      localStorage.setItem("admin_token", data.token);
      isAuthenticated = true;
      password = "";
      
      // Load initial data
      await Promise.all([loadReports(), loadStats()]);
    } catch (e: any) {
      loginError = e.message || "Login failed";
    } finally {
      isLoggingIn = false;
    }
  }

  async function handleLogout() {
    if (authToken) {
      try {
        await fetch("/api/v1/admin/logout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token: authToken })
        });
      } catch (e) {
        // Ignore errors on logout
      }
    }
    
    authToken = null;
    localStorage.removeItem("admin_token");
    isAuthenticated = false;
    reports = [];
    stats = null;
  }

  async function loadReports() {
    if (!authToken) return;
    
    isLoadingReports = true;
    errorMsg = null;

    try {
      const params = new URLSearchParams();
      if (filterFlaggedOnly) params.append("flagged_only", "true");
      if (filterHasViolations !== null) params.append("has_violations", String(filterHasViolations));
      params.append("limit", "100");

      const res = await fetch(`/api/v1/admin/reports?${params}`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });

      if (!res.ok) {
        if (res.status === 401) {
          handleLogout();
          return;
        }
        throw new Error("Failed to load reports");
      }

      const data = await res.json();
      let fetchedReports = data.reports || [];
      
      // Apply pending approval filter on client side
      if (filterPendingApproval) {
        fetchedReports = fetchedReports.filter((r: any) => 
          r.is_violation && !r.admin_reviewed
        );
      }
      
      reports = fetchedReports;
    } catch (e: any) {
      errorMsg = e.message || "Failed to load reports";
    } finally {
      isLoadingReports = false;
    }
  }

  async function loadStats() {
    if (!authToken) return;
    
    isLoadingStats = true;

    try {
      const res = await fetch("/api/v1/admin/stats", {
        headers: { Authorization: `Bearer ${authToken}` }
      });

      if (!res.ok) throw new Error("Failed to load stats");

      const data = await res.json();
      stats = data.stats;
    } catch (e: any) {
      console.error("Failed to load stats:", e);
    } finally {
      isLoadingStats = false;
    }
  }

  async function toggleFlag(reportId: number, currentFlag: boolean) {
    if (!authToken) return;

    try {
      const res = await fetch(`/api/v1/admin/reports/${reportId}/flag`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ flagged: !currentFlag })
      });

      if (!res.ok) throw new Error("Failed to update flag");

      await loadReports();
      await loadStats();
    } catch (e: any) {
      errorMsg = e.message || "Failed to update flag";
    }
  }

  async function approveReport(reportId: number, approve: boolean) {
    if (!authToken) return;

    try {
      const res = await fetch(`/api/v1/admin/reports/${reportId}/approve`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ approved: approve })
      });

      if (!res.ok) throw new Error("Failed to approve report");

      await loadReports();
      await loadStats();
      if (showDetailDialog) {
        showDetailDialog = false;
      }
    } catch (e: any) {
      errorMsg = e.message || "Failed to approve report";
    }
  }

  function viewReportDetail(report: any) {
    selectedReport = report;
    showDetailDialog = true;
  }

  function formatDate(dateStr: string) {
    try {
      return new Date(dateStr).toLocaleString();
    } catch {
      return dateStr;
    }
  }

  // Check for existing token on mount
  $effect(() => {
    const token = localStorage.getItem("admin_token");
    if (token) {
      authToken = token;
      isAuthenticated = true;
      loadReports();
      loadStats();
    }
  });

  // Reload when filters change
  $effect(() => {
    if (isAuthenticated) {
      filterFlaggedOnly;
      filterHasViolations;
      filterPendingApproval;
      loadReports();
    }
  });
</script>

<main class="min-h-screen py-8 bg-muted/30">
  <div class="container max-w-7xl mx-auto px-4">
    {#if !isAuthenticated}
      <!-- Login Form -->
      <div class="flex items-center justify-center min-h-[80vh]">
        <div class="w-full max-w-md space-y-4">
          <Card>
            <CardHeader>
              <div class="flex items-center gap-3 mb-2">
                <div class="p-3 rounded-lg bg-primary/10 text-primary">
                  <Shield size={28} />
                </div>
                <div>
                  <CardTitle>Admin Login</CardTitle>
                  <p class="text-sm text-muted-foreground mt-1">Enter admin password to continue</p>
                </div>
              </div>
            </CardHeader>
          <CardContent>
            <form onsubmit={(e) => { e.preventDefault(); handleLogin(); }}>
              <div class="space-y-4">
                <div>
                  <label for="password" class="block text-sm font-medium mb-2">Password</label>
                  <input
                    id="password"
                    type="password"
                    bind:value={password}
                    class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="Enter admin password"
                    disabled={isLoggingIn}
                  />
                </div>
                
                {#if loginError}
                  <Alert variant="destructive">
                    <AlertDescription>{loginError}</AlertDescription>
                  </Alert>
                {/if}

                <Button type="submit" class="w-full" disabled={isLoggingIn}>
                  {isLoggingIn ? "Logging in..." : "Login"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
        
        <div class="text-center">
          <a href="/">
            <Button variant="ghost">
              ← Back to Home
            </Button>
          </a>
        </div>
      </div>
      </div>
    {:else}
      <!-- Admin Dashboard -->
      <div class="space-y-6">
        <!-- Header -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="p-2 rounded-lg bg-primary/10 text-primary">
              <Shield size={28} />
            </div>
            <div>
              <h1 class="text-3xl font-bold">Admin Dashboard</h1>
              <p class="text-sm text-muted-foreground">Manage violation reports and system data</p>
            </div>
          </div>
          <Button variant="outline" onclick={handleLogout}>
            <LogOut size={18} />
            Logout
          </Button>
        </div>

        <!-- Stats Cards -->
        {#if stats}
          <div class="grid md:grid-cols-2 lg:grid-cols-5 gap-4">
            <Card>
              <CardContent class="pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">Total Reports</p>
                    <p class="text-2xl font-bold">{stats.total_reports}</p>
                  </div>
                  <FileText size={24} class="text-muted-foreground" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent class="pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">Pending Approval</p>
                    <p class="text-2xl font-bold text-amber-600">{stats.pending_approval || 0}</p>
                  </div>
                  <Clock size={24} class="text-amber-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent class="pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">Approved</p>
                    <p class="text-2xl font-bold text-green-600">{stats.approved_reports || 0}</p>
                  </div>
                  <CheckCircle size={24} class="text-green-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent class="pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">Flagged</p>
                    <p class="text-2xl font-bold text-destructive">{stats.flagged_reports}</p>
                  </div>
                  <Flag size={24} class="text-destructive" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent class="pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">With Violations</p>
                    <p class="text-2xl font-bold text-destructive">{stats.reports_with_violations}</p>
                  </div>
                  <AlertCircle size={24} class="text-destructive" />
                </div>
              </CardContent>
            </Card>
          </div>
        {/if}

        <!-- Filters and Actions -->
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center gap-4 flex-wrap">
              <div class="flex items-center gap-2">
                <Filter size={18} class="text-muted-foreground" />
                <span class="text-sm font-medium">Filters:</span>
              </div>
              
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" bind:checked={filterFlaggedOnly} class="rounded" />
                <span class="text-sm">Flagged Only</span>
              </label>
              
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" bind:checked={filterPendingApproval} class="rounded" />
                <span class="text-sm">Pending Approval</span>
              </label>
              
              <select 
                bind:value={filterHasViolations}
                class="px-3 py-1.5 border rounded-lg text-sm"
              >
                <option value={null}>All Reports</option>
                <option value={true}>With Violations</option>
                <option value={false}>No Violations</option>
              </select>

              <Button variant="outline" size="sm" onclick={loadReports} disabled={isLoadingReports}>
                <RefreshCw size={16} class={isLoadingReports ? "animate-spin" : ""} />
                Refresh
              </Button>
            </div>
          </CardContent>
        </Card>

        {#if errorMsg}
          <Alert variant="destructive">
            <AlertDescription>{errorMsg}</AlertDescription>
          </Alert>
        {/if}

        <!-- Reports Table -->
        <Card>
          <CardHeader>
            <CardTitle>Violation Reports</CardTitle>
          </CardHeader>
          <CardContent>
            {#if isLoadingReports}
              <div class="text-center py-12">
                <RefreshCw size={32} class="animate-spin mx-auto mb-2 text-muted-foreground" />
                <p class="text-sm text-muted-foreground">Loading reports...</p>
              </div>
            {:else if reports.length === 0}
              <div class="text-center py-12">
                <FileText size={48} class="mx-auto mb-4 text-muted-foreground" />
                <p class="text-muted-foreground">No reports found</p>
              </div>
            {:else}
              <div class="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>License Plate</TableHead>
                      <TableHead>Violations</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Confidence</TableHead>
                      <TableHead class="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {#each reports as report}
                      <TableRow>
                        <TableCell class="font-mono text-sm">{report.id}</TableCell>
                        <TableCell class="text-sm">{formatDate(report.reported_timestamp)}</TableCell>
                        <TableCell>
                          {#if report.license_plate}
                            <span class="font-mono text-sm">{report.license_plate}</span>
                          {:else}
                            <span class="text-muted-foreground text-sm">—</span>
                          {/if}
                        </TableCell>
                        <TableCell>
                          {#if report.is_violation && report.violations?.length > 0}
                            <div class="flex gap-1 flex-wrap">
                              {#each report.violations.slice(0, 2) as v}
                                <Badge variant="destructive" class="text-xs">{v?.name ?? v}</Badge>
                              {/each}
                              {#if report.violations.length > 2}
                                <Badge variant="outline" class="text-xs">+{report.violations.length - 2}</Badge>
                              {/if}
                            </div>
                          {:else}
                            <Badge variant="outline" class="text-xs">None</Badge>
                          {/if}
                        </TableCell>
                        <TableCell>
                          <div class="flex gap-1 flex-wrap">
                            {#if report.admin_approved}
                              <Badge variant="default" class="bg-green-600 text-xs">
                                <Check size={12} />
                                Approved
                              </Badge>
                            {:else if report.admin_reviewed}
                              <Badge variant="destructive" class="text-xs">
                                <X size={12} />
                                Rejected
                              </Badge>
                            {:else if report.is_violation}
                              <Badge variant="default" class="bg-amber-600 text-xs">
                                <Clock size={12} />
                                Pending
                              </Badge>
                            {/if}
                            {#if report.needs_manual_verification}
                              <Badge variant="destructive" class="text-xs">
                                <Flag size={12} />
                                Flagged
                              </Badge>
                            {/if}
                            {#if !report.is_violation}
                              <Badge variant="outline" class="text-xs text-green-600">Clean</Badge>
                            {/if}
                          </div>
                        </TableCell>
                        <TableCell>
                          <span class="text-sm">{(report.confidence_score * 100).toFixed(0)}%</span>
                        </TableCell>
                        <TableCell class="text-right">
                          <div class="flex gap-2 justify-end">
                            <Button variant="ghost" size="sm" onclick={() => viewReportDetail(report)}>
                              <Eye size={16} />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onclick={() => toggleFlag(report.id, report.needs_manual_verification)}
                            >
                              <Flag size={16} class={report.needs_manual_verification ? "fill-current text-amber-500" : ""} />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    {/each}
                  </TableBody>
                </Table>
              </div>
            {/if}
          </CardContent>
        </Card>
      </div>
    {/if}
  </div>
</main>

<!-- Report Detail Dialog -->
{#if showDetailDialog && selectedReport}
  <Dialog bind:open={showDetailDialog}>
    <DialogContent class="max-w-3xl max-h-[80vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Report #{selectedReport.id}</DialogTitle>
      </DialogHeader>
      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm font-medium text-muted-foreground">Timestamp</p>
            <p class="text-sm">{formatDate(selectedReport.reported_timestamp)}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Reporter Phone</p>
            <p class="text-sm font-mono">{selectedReport.reporter_phone || "Web Upload"}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">License Plate</p>
            <p class="text-sm font-mono">{selectedReport.license_plate || "Not detected"}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Confidence</p>
            <p class="text-sm">{(selectedReport.confidence_score * 100).toFixed(1)}%</p>
          </div>
        </div>

        {#if selectedReport.title}
          <div>
            <p class="text-sm font-medium text-muted-foreground mb-1">Title</p>
            <p class="text-sm">{selectedReport.title}</p>
          </div>
        {/if}

        {#if selectedReport.short_description}
          <div>
            <p class="text-sm font-medium text-muted-foreground mb-1">Summary</p>
            <p class="text-sm">{selectedReport.short_description}</p>
          </div>
        {/if}

        {#if selectedReport.detailed_description}
          <div>
            <p class="text-sm font-medium text-muted-foreground mb-1">Detailed Description</p>
            <p class="text-sm">{selectedReport.detailed_description}</p>
          </div>
        {/if}

        {#if selectedReport.violations?.length > 0}
          <div>
            <p class="text-sm font-medium text-muted-foreground mb-2">Detected Violations</p>
            <div class="space-y-2">
              {#each selectedReport.violations as v}
                <div class="p-3 border rounded-lg bg-muted/30">
                  <div class="flex items-start justify-between mb-1">
                    <span class="font-medium text-sm">{v.name}</span>
                    {#if v.fine_amount}
                      <Badge variant="destructive">₹{v.fine_amount}</Badge>
                    {/if}
                  </div>
                  {#if v.section}
                    <p class="text-xs text-muted-foreground">Section: {v.section}</p>
                  {/if}
                </div>
              {/each}
            </div>
          </div>
        {/if}

        {#if selectedReport.reported_image}
          <div>
            <p class="text-sm font-medium text-muted-foreground mb-2">Image</p>
            <img src={selectedReport.reported_image} alt="Report" class="w-full rounded-lg border" />
          </div>
        {/if}

        <!-- Approval Actions -->
        {#if selectedReport.is_violation && !selectedReport.admin_reviewed}
          <div class="flex gap-3 pt-4 border-t">
            <Button 
              class="flex-1 bg-green-600 hover:bg-green-700"
              onclick={() => approveReport(selectedReport.id, true)}
            >
              <Check size={18} />
              Approve Report
            </Button>
            <Button 
              variant="destructive"
              class="flex-1"
              onclick={() => approveReport(selectedReport.id, false)}
            >
              <X size={18} />
              Reject Report
            </Button>
          </div>
        {:else if selectedReport.admin_approved}
          <Alert class="border-green-600 bg-green-50 dark:bg-green-950/20">
            <CheckCircle size={18} class="text-green-600" />
            <AlertDescription class="text-green-800 dark:text-green-200">
              This report has been approved by an admin.
            </AlertDescription>
          </Alert>
        {:else if selectedReport.admin_reviewed}
          <Alert variant="destructive">
            <X size={18} />
            <AlertDescription>
              This report has been rejected by an admin.
            </AlertDescription>
          </Alert>
        {/if}
      </div>
    </DialogContent>
  </Dialog>
{/if}
