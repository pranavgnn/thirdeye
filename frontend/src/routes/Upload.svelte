<script lang="ts">
  import Button from "@/components/ui/Button.svelte";
  import Card from "@/components/ui/Card.svelte";
  import CardHeader from "@/components/ui/CardHeader.svelte";
  import CardTitle from "@/components/ui/CardTitle.svelte";
  import CardDescription from "@/components/ui/CardDescription.svelte";
  import CardContent from "@/components/ui/CardContent.svelte";
  import Alert from "@/components/ui/Alert.svelte";
  import AlertDescription from "@/components/ui/AlertDescription.svelte";
  import Badge from "@/components/ui/Badge.svelte";
  import { Upload as UploadIcon, Image as ImageIcon, AlertCircle, CheckCircle, Loader2, ArrowLeft, FileUp } from "lucide-svelte";

  let isDragging = $state(false);
  let selectedFile = $state<File | null>(null);
  let previewUrl = $state<string | null>(null);
  let isAnalyzing = $state(false);
  let analysisResult = $state<any>(null);
  let errorMsg = $state<string | null>(null);

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    isDragging = true;
  }
  function handleDragLeave() { isDragging = false; }
  function handleDrop(event: DragEvent) {
    event.preventDefault();
    isDragging = false;
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) handleFileSelection(files[0]);
  }
  function handleFileInput(event: Event) {
    const files = (event.target as HTMLInputElement).files;
    if (files && files.length > 0) handleFileSelection(files[0]);
  }
  function handleFileSelection(file: File) {
    if (!file.type.startsWith("image/")) { errorMsg = "Please select an image file"; return; }
    if (file.size > 10 * 1024 * 1024) { errorMsg = "Max size is 10MB"; return; }
    selectedFile = file; errorMsg = null; analysisResult = null;
    const reader = new FileReader();
    reader.onload = (e) => { previewUrl = e.target?.result as string; };
    reader.readAsDataURL(file);
  }
  function clearSelection() {
    selectedFile = null; previewUrl = null; analysisResult = null; errorMsg = null;
  }
  async function analyzeImage() {
    if (!selectedFile) return;
    isAnalyzing = true; errorMsg = null;
    try {
      const form = new FormData();
      form.append("file", selectedFile);
      const res = await fetch("/api/v1/analyze", { method: "POST", body: form });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Request failed with ${res.status}`);
      }
      const data = await res.json();
      analysisResult = data.result || data; // support both shapes
    } catch (e: any) {
      errorMsg = e.message || String(e);
    } finally { isAnalyzing = false; }
  }
</script>

<main class="min-h-screen py-16">
  <div class="container max-w-4xl mx-auto px-4">
    <div class="mb-8">
      <h1 class="text-4xl font-bold tracking-tight mb-2 flex items-center gap-3">
        <UploadIcon size={36} /> Upload & Analyze Image
      </h1>
      <p class="text-muted-foreground">Drag and drop a photo or select a file to analyze for traffic violations.</p>
    </div>

    {#if !selectedFile}
      <Card>
        <CardContent class="p-0">
          <div class="relative border-2 border-dashed rounded-xl transition-all {isDragging ? 'border-primary bg-primary/5 scale-[0.98]' : 'border-border'}"
               ondragover={handleDragOver} ondragleave={handleDragLeave} ondrop={handleDrop}>
            <input type="file" accept="image/*" onchange={handleFileInput}
                   class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
            <div class="flex flex-col items-center justify-center py-16 px-8">
              <div class="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-primary/10 text-primary mb-6 {isDragging ? 'scale-110' : ''}">
                {#if isDragging}<FileUp size={40} />{:else}<ImageIcon size={40} />{/if}
              </div>
              <h3 class="text-xl font-semibold mb-2">{isDragging ? 'Drop your image here' : 'Upload an image'}</h3>
              <p class="text-muted-foreground text-center mb-6 max-w-md">Drag and drop your image here, or click to browse. JPG/PNG up to 10MB.</p>
              <Button size="lg"><UploadIcon size={20} /> Choose File</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    {:else}
      <div class="space-y-6">
        <Card>
          <CardHeader>
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>Selected Image</CardTitle>
                <CardDescription>{selectedFile.name} ({(selectedFile.size/1024).toFixed(1)} KB)</CardDescription>
              </div>
              <Button variant="ghost" size="sm" onclick={clearSelection}>Clear</Button>
            </div>
          </CardHeader>
          <CardContent>
            {#if previewUrl}
              <div class="rounded-lg overflow-hidden border">
                <img src={previewUrl} alt="Preview" class="w-full h-auto max-h-96 object-contain bg-muted" />
              </div>
            {/if}
            {#if !analysisResult && !isAnalyzing}
              <div class="mt-6 flex justify-center">
                <Button size="lg" onclick={analyzeImage} disabled={isAnalyzing}>Analyze Image</Button>
              </div>
            {/if}
          </CardContent>
        </Card>

        {#if errorMsg}
          <Alert variant="destructive"><AlertDescription>{errorMsg}</AlertDescription></Alert>
        {/if}

        {#if isAnalyzing}
          <Card><CardContent>
            <div class="flex flex-col items-center justify-center py-12">
              <Loader2 size={48} class="animate-spin text-primary mb-4" />
              <h3 class="text-xl font-semibold mb-2">Analyzing Image...</h3>
              <p class="text-muted-foreground text-center max-w-md">This may take a few moments.</p>
            </div>
          </CardContent></Card>
        {/if}

        {#if analysisResult && !isAnalyzing}
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                {#if analysisResult.is_violation}
                  <AlertCircle size={22} class="text-destructive" />
                {:else}
                  <CheckCircle size={22} class="text-green-600" />
                {/if}
                {analysisResult.title || 'Analysis Complete'}
              </CardTitle>
              {#if analysisResult.license_plate}
                <CardDescription class="font-mono">License Plate: {analysisResult.license_plate}</CardDescription>
              {/if}
            </CardHeader>
            <CardContent class="space-y-4">
              {#if analysisResult.short_description}
                <div>
                  <h4 class="font-semibold mb-1">Summary</h4>
                  <p class="text-sm text-muted-foreground">{analysisResult.short_description}</p>
                </div>
              {/if}
              {#if analysisResult.violations && analysisResult.violations.length > 0}
                <div class="space-y-3">
                  <h4 class="font-semibold">Detected Violations</h4>
                  <div class="flex flex-wrap gap-2">
                    {#each analysisResult.violations as v}
                      <Badge variant="destructive">{v?.name ?? v}</Badge>
                    {/each}
                  </div>
                </div>
              {/if}
              <div class="flex gap-3 pt-4 border-t">
                <Button onclick={clearSelection} variant="outline" class="flex-1">Analyze Another Image</Button>
              </div>
            </CardContent>
          </Card>
        {/if}
      </div>
    {/if}

    <div class="text-center mt-8">
      <a href="/"><Button variant="outline"><ArrowLeft size={18}/> Back to Home</Button></a>
    </div>
  </div>
</main>
