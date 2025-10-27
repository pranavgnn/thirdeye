<script lang="ts">
  import Button from "@/components/ui/Button.svelte";
  import Card from "@/components/ui/Card.svelte";
  import CardHeader from "@/components/ui/CardHeader.svelte";
  import CardTitle from "@/components/ui/CardTitle.svelte";
  import CardDescription from "@/components/ui/CardDescription.svelte";
  import CardContent from "@/components/ui/CardContent.svelte";
  import Badge from "@/components/ui/Badge.svelte";
  import Alert from "@/components/ui/Alert.svelte";
  import AlertDescription from "@/components/ui/AlertDescription.svelte";
  import {
    Upload as UploadIcon,
    Image as ImageIcon,
    AlertCircle,
    CheckCircle,
    Loader2,
    X,
    ArrowLeft,
    FileUp,
    Sparkles,
  } from "lucide-svelte";

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

  function handleDragLeave() {
    isDragging = false;
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    isDragging = false;

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      handleFileSelection(files[0]);
    }
  }

  function handleFileInput(event: Event) {
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length > 0) {
      handleFileSelection(files[0]);
    }
  }

  function handleFileSelection(file: File) {
    // Validate file type
    if (!file.type.startsWith("image/")) {
      errorMsg = "Please select a valid image file";
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      errorMsg = "Image size must be less than 10MB";
      return;
    }

    selectedFile = file;
    errorMsg = null;
    analysisResult = null;

    // Create preview URL
    const reader = new FileReader();
    reader.onload = (e) => {
      previewUrl = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }

  function clearSelection() {
    selectedFile = null;
    previewUrl = null;
    analysisResult = null;
    errorMsg = null;
  }

  async function analyzeImage() {
    if (!selectedFile) return;

    isAnalyzing = true;
    errorMsg = null;

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch("/api/v1/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `Request failed with ${response.status}`);
      }

      const data = await response.json();
      analysisResult = data.result;
    } catch (err: any) {
      errorMsg = err.message || String(err);
    } finally {
      isAnalyzing = false;
    }
  }

  function formatCurrency(amount: number) {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(amount);
  }
</script>

<main class="min-h-screen py-16">
  <div class="container max-w-4xl mx-auto px-4">
    <div class="mb-8">
      <h1 class="text-4xl font-bold tracking-tight mb-2 flex items-center gap-3">
        <UploadIcon size={36} />
        Analyze Traffic Violation
      </h1>
      <p class="text-muted-foreground">
        Upload or drag and drop an image to analyze for traffic violations
      </p>
    </div>

    {#if !selectedFile}
      <!-- Upload Area -->
      <Card>
        <CardContent class="p-0">
          <div
            class="relative border-2 border-dashed rounded-xl transition-all {isDragging
              ? 'border-primary bg-primary/5 scale-[0.98]'
              : 'border-border'}"
            ondragover={handleDragOver}
            ondragleave={handleDragLeave}
            ondrop={handleDrop}
          >
            <input
              type="file"
              accept="image/*"
              onchange={handleFileInput}
              class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              id="file-input"
            />
            <div class="flex flex-col items-center justify-center py-16 px-8">
              <div
                class="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-primary/10 text-primary mb-6 transition-transform {isDragging
                  ? 'scale-110'
                  : ''}"
              >
                {#if isDragging}
                  <FileUp size={40} />
                {:else}
                  <ImageIcon size={40} />
                {/if}
              </div>

              <h3 class="text-xl font-semibold mb-2">
                {isDragging ? "Drop your image here" : "Upload an image"}
              </h3>
              <p class="text-muted-foreground text-center mb-6 max-w-md">
                Drag and drop your image here, or click to browse. Supports JPG,
                PNG, and other image formats (max 10MB).
              </p>

              <Button size="lg">
                <UploadIcon size={20} />
                Choose File
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <div
        class="bg-amber-50 dark:bg-amber-950/30 border-l-4 border-amber-500 p-4 rounded-lg mt-6"
      >
        <div class="flex items-start gap-3">
          <AlertCircle
            size={20}
            class="text-amber-600 dark:text-amber-400 shrink-0 mt-0.5"
          />
          <div>
            <p class="text-sm text-amber-900 dark:text-amber-200">
              <strong>Educational Use Only:</strong> This service is for educational
              purposes. All reports require manual verification by authorities.
            </p>
          </div>
        </div>
      </div>
    {:else}
      <!-- Preview and Analysis -->
      <div class="space-y-6">
        <!-- Image Preview Card -->
        <Card>
          <CardHeader>
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>Selected Image</CardTitle>
                <CardDescription
                  >{selectedFile.name} ({(selectedFile.size / 1024).toFixed(
                    1
                  )} KB)</CardDescription
                >
              </div>
              <Button variant="ghost" size="sm" onclick={clearSelection}>
                <X size={18} />
                Clear
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {#if previewUrl}
              <div class="rounded-lg overflow-hidden border">
                <img
                  src={previewUrl}
                  alt="Preview"
                  class="w-full h-auto max-h-96 object-contain bg-muted"
                />
              </div>
            {/if}

            {#if !analysisResult && !isAnalyzing}
              <div class="mt-6 flex justify-center">
                <Button size="lg" onclick={analyzeImage} disabled={isAnalyzing}>
                  <Sparkles size={20} />
                  Analyze Image
                </Button>
              </div>
            {/if}
          </CardContent>
        </Card>

        <!-- Error Message -->
        {#if errorMsg}
          <Alert variant="destructive">
            <AlertCircle size={18} />
            <AlertDescription>{errorMsg}</AlertDescription>
          </Alert>
        {/if}

        <!-- Loading State -->
        {#if isAnalyzing}
          <Card>
            <CardContent>
              <div class="flex flex-col items-center justify-center py-12">
                <Loader2 size={48} class="animate-spin text-primary mb-4" />
                <h3 class="text-xl font-semibold mb-2">Analyzing Image...</h3>
                <p class="text-muted-foreground text-center max-w-md">
                  Our AI is examining the image for traffic violations. This may
                  take a few moments.
                </p>
              </div>
            </CardContent>
          </Card>
        {/if}

        <!-- Analysis Results -->
        {#if analysisResult && !isAnalyzing}
          <!-- Location Warning (if not India) -->
          {#if !analysisResult.is_india_location && analysisResult.location_confidence > 0.99}
            <Alert variant="destructive" class="mb-6">
              <AlertCircle size={20} />
              <AlertDescription>
                <strong>⚠️ WARNING:</strong> This image does not appear to be from
                India (confidence: {Math.round(analysisResult.location_confidence * 100)}%).
                This application is designed exclusively for Indian traffic scenarios.
                The analysis may not be accurate or applicable.
              </AlertDescription>
            </Alert>
          {/if}

          <Card>
            <CardHeader>
              <div class="flex items-center justify-between">
                <CardTitle class="flex items-center gap-2">
                  {#if analysisResult.is_violation}
                    <AlertCircle size={24} class="text-destructive" />
                  {:else}
                    <CheckCircle size={24} class="text-green-500" />
                  {/if}
                  {analysisResult.title || "Analysis Complete"}
                </CardTitle>
                {#if analysisResult.is_violation}
                  <Badge variant="destructive">Violation Detected</Badge>
                {:else}
                  <Badge variant="secondary">No Violation</Badge>
                {/if}
              </div>
              {#if analysisResult.license_plate && analysisResult.license_plate_confidence >= 0.7}
                <CardDescription class="text-base font-mono flex items-center gap-2">
                  License Plate: {analysisResult.license_plate}
                  <Badge variant="secondary" class="text-xs">
                    {Math.round(analysisResult.license_plate_confidence * 100)}% confidence
                  </Badge>
                </CardDescription>
              {:else if analysisResult.vehicle_detected}
                <CardDescription class="text-base text-muted-foreground">
                  License plate not detected or low confidence
                </CardDescription>
              {/if}
            </CardHeader>
            <CardContent class="space-y-6">
              <!-- Confidence Score -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium">Analysis Confidence</span>
                  <span class="text-sm font-semibold"
                    >{Math.round(analysisResult.confidence_score * 100)}%</span
                  >
                </div>
                <div class="w-full h-3 bg-muted rounded-full overflow-hidden">
                  <div
                    class="h-full transition-all {analysisResult.confidence_score >=
                    0.7
                      ? 'bg-green-500'
                      : analysisResult.confidence_score >= 0.5
                        ? 'bg-amber-500'
                        : 'bg-destructive'}"
                    style="width: {analysisResult.confidence_score * 100}%"
                  ></div>
                </div>
              </div>

              <!-- Location Detection -->
              {#if analysisResult.is_india_location}
                <div class="p-3 border rounded-lg bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-800">
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-green-900 dark:text-green-100">
                      ✓ Detected as Indian traffic scenario
                    </span>
                    <Badge variant="secondary" class="text-xs">
                      {Math.round(analysisResult.location_confidence * 100)}% confidence
                    </Badge>
                  </div>
                </div>
              {:else if analysisResult.location_confidence > 0.5}
                <div class="p-3 border rounded-lg bg-amber-50 dark:bg-amber-950/20 border-amber-200 dark:border-amber-800">
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-amber-900 dark:text-amber-100">
                      ⚠ Uncertain location - may not be India
                    </span>
                    <Badge variant="secondary" class="text-xs">
                      {Math.round((1 - analysisResult.location_confidence) * 100)}% India likelihood
                    </Badge>
                  </div>
                </div>
              {/if}

              <!-- Description -->
              {#if analysisResult.short_description}
                <div>
                  <h4 class="font-semibold mb-2">Summary</h4>
                  <p class="text-sm text-muted-foreground">
                    {analysisResult.short_description}
                  </p>
                </div>
              {/if}

              {#if analysisResult.detailed_description}
                <div>
                  <h4 class="font-semibold mb-2">Detailed Analysis</h4>
                  <p class="text-sm text-muted-foreground">
                    {analysisResult.detailed_description}
                  </p>
                </div>
              {/if}

              <!-- Violations -->
              {#if analysisResult.violations && analysisResult.violations.length > 0}
                <div>
                  <h4 class="font-semibold mb-3">Detected Violations</h4>
                  <div class="space-y-3">
                    {#each analysisResult.violations as violation}
                      <div class="p-4 border rounded-lg bg-muted/30">
                        <div class="flex items-start justify-between mb-2">
                          <span class="font-medium">{violation.name}</span>
                          {#if violation.fine_amount}
                            <Badge variant="destructive"
                              >{formatCurrency(violation.fine_amount)}</Badge
                            >
                          {/if}
                        </div>
                        <div class="space-y-1">
                          {#if violation.category}
                            <p class="text-xs text-muted-foreground">
                              Category: {violation.category}
                            </p>
                          {/if}
                          {#if violation.section}
                            <p class="text-xs text-muted-foreground">
                              Section: {violation.section}
                            </p>
                          {/if}
                        </div>
                      </div>
                    {/each}
                  </div>
                </div>
              {/if}

              <!-- Actions -->
              <div class="flex gap-3 pt-4 border-t">
                <Button onclick={clearSelection} variant="outline" class="flex-1">
                  <UploadIcon size={18} />
                  Analyze Another Image
                </Button>
              </div>
            </CardContent>
          </Card>
        {/if}
      </div>
    {/if}

    <!-- Back to Home -->
    <div class="text-center mt-8">
      <a href="/">
        <Button variant="outline">
          <ArrowLeft size={18} />
          Back to Home
        </Button>
      </a>
    </div>
  </div>
</main>
