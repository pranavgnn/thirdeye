<script lang="ts">
  import Button from "@/components/ui/Button.svelte";
  import Badge from "@/components/ui/Badge.svelte";
  import {
    MessageCircle,
    Scan,
    FileCheck,
    Sparkles,
    Zap,
    Shield,
    Lock,
    AlertCircle,
    ShieldCheck,
  } from "lucide-svelte";

  const whatsappNumber = "15551856117"; // +1 (555) 185-6117
  const whatsappUrl = `https://wa.me/${whatsappNumber}`;
</script>

<main class="min-h-screen">
  <div class="container max-w-5xl mx-auto py-16 px-4">
    <!-- Admin Login Button in Header -->
    <div class="flex justify-end mb-8">
      <a href="/admin">
        <Button variant="ghost" size="sm">
          <ShieldCheck size={18} />
          Admin Login
        </Button>
      </a>
    </div>
    <div class="text-center mb-16">
      <div
        class="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-medium mb-6"
      >
        <Sparkles size={16} />
        <span>AI-Powered Analysis</span>
      </div>
      <h1 class="text-6xl font-bold tracking-tight mb-4">ThirdEye</h1>
      <p class="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
        Detect and report traffic violations instantly using AI-powered image
        analysis via WhatsApp
      </p>
      <div class="flex gap-4 justify-center flex-wrap">
        <a href="/upload">
          <Button size="lg">
            <Scan size={20} />
            Upload & Analyze
          </Button>
        </a>
        <a href={whatsappUrl} target="_blank" rel="noopener noreferrer">
          <Button size="lg" variant="outline">
            <MessageCircle size={20} />
            Chat on WhatsApp
          </Button>
        </a>
      </div>
    </div>

    <div
      class="bg-amber-50 dark:bg-amber-950/30 border-l-4 border-amber-500 p-4 rounded-lg mb-12"
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

    <div class="mb-16">
      <h2 class="text-3xl font-bold mb-8 text-center">How It Works</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div class="text-center">
          <div
            class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 text-primary mb-4"
          >
            <MessageCircle size={32} />
          </div>
          <h3 class="text-xl font-semibold mb-2">1. Send Photo</h3>
          <p class="text-muted-foreground">
            Submit a traffic violation image via WhatsApp to our bot
          </p>
        </div>
        <div class="text-center">
          <div
            class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 text-primary mb-4"
          >
            <Scan size={32} />
          </div>
          <h3 class="text-xl font-semibold mb-2">2. AI Analysis</h3>
          <p class="text-muted-foreground">
            Our system analyzes the image using Google Gemini Vision
          </p>
        </div>
        <div class="text-center">
          <div
            class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 text-primary mb-4"
          >
            <FileCheck size={32} />
          </div>
          <h3 class="text-xl font-semibold mb-2">3. Get Report</h3>
          <p class="text-muted-foreground">
            Receive an instant summary with violation details
          </p>
        </div>
      </div>
    </div>

    <div class="mb-16">
      <h2 class="text-3xl font-bold mb-8 text-center">Key Features</h2>
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          class="p-6 rounded-xl border bg-card hover:shadow-lg transition-shadow"
        >
          <div
            class="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10 text-primary mb-3"
          >
            <Sparkles size={24} />
          </div>
          <h3 class="font-semibold mb-2">AI-Powered</h3>
          <p class="text-sm text-muted-foreground">
            Advanced computer vision analysis
          </p>
        </div>
        <div
          class="p-6 rounded-xl border bg-card hover:shadow-lg transition-shadow"
        >
          <div
            class="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10 text-primary mb-3"
          >
            <Zap size={24} />
          </div>
          <h3 class="font-semibold mb-2">Lightning Fast</h3>
          <p class="text-sm text-muted-foreground">
            Instant WhatsApp responses
          </p>
        </div>
        <div
          class="p-6 rounded-xl border bg-card hover:shadow-lg transition-shadow"
        >
          <div
            class="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10 text-primary mb-3"
          >
            <Shield size={24} />
          </div>
          <h3 class="font-semibold mb-2">Secure</h3>
          <p class="text-sm text-muted-foreground">End-to-end encrypted</p>
        </div>
        <div
          class="p-6 rounded-xl border bg-card hover:shadow-lg transition-shadow"
        >
          <div
            class="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10 text-primary mb-3"
          >
            <Lock size={24} />
          </div>
          <h3 class="font-semibold mb-2">Privacy First</h3>
          <p class="text-sm text-muted-foreground">GDPR compliant</p>
        </div>
      </div>
    </div>

    <div class="bg-muted/50 rounded-2xl p-8 mb-12">
      <h2 class="text-2xl font-bold mb-4">Meta Business Verification</h2>
      <p class="text-muted-foreground mb-4">
        This WhatsApp Business Account is verified by Meta and complies with
        their terms of service.
      </p>
      <div class="flex flex-wrap gap-2">
        <Badge class="text-sm">WhatsApp Business API</Badge>
        <Badge class="text-sm">Meta Verified</Badge>
        <Badge class="text-sm">GDPR Compliant</Badge>
      </div>
    </div>

    <div class="text-center space-x-6">
      <a
        href="/upload"
        class="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
      >
        Upload & Analyze
      </a>
      <span class="text-muted-foreground">•</span>
      <a
        href="/privacy"
        class="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
      >
        Privacy Policy
      </a>
      <span class="text-muted-foreground">•</span>
      <a
        href="/admin"
        class="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
      >
        Admin
      </a>
    </div>
  </div>
</main>
