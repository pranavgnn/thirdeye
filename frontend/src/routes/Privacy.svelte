<script lang="ts">
  import Button from "@/components/ui/Button.svelte";
  import { ArrowLeft, Shield, Database, Lock, Users, FileText, Mail } from "lucide-svelte";
</script>

<main class="min-h-screen py-16">
  <div class="container max-w-4xl mx-auto px-4">
    <div class="mb-12">
      <h1 class="text-5xl font-bold tracking-tight mb-3">Privacy Policy</h1>
      <p class="text-lg text-muted-foreground">Last updated: October 2025</p>
    </div>

    <div class="space-y-8">
      <section>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 rounded-lg bg-primary/10 text-primary">
            <FileText size={24} />
          </div>
          <h2 class="text-2xl font-bold">Overview</h2>
        </div>
        <p class="text-muted-foreground leading-relaxed">
          This privacy policy explains how we collect, use, and protect your data when you interact
          with our ThirdEye service via WhatsApp.
        </p>
      </section>

      <section>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 rounded-lg bg-primary/10 text-primary">
            <Database size={24} />
          </div>
          <h2 class="text-2xl font-bold">Information We Collect</h2>
        </div>
        <p class="text-muted-foreground mb-3">When you use our service, we collect:</p>
        <ul class="space-y-2 text-muted-foreground">
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Your WhatsApp phone number</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Images you send to us for analysis</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>AI-generated analysis reports</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Timestamps of interactions</span>
          </li>
        </ul>
      </section>

      <section>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 rounded-lg bg-primary/10 text-primary">
            <Users size={24} />
          </div>
          <h2 class="text-2xl font-bold">How We Use Your Information</h2>
        </div>
        <p class="text-muted-foreground mb-3">We use your information to:</p>
        <ul class="space-y-2 text-muted-foreground">
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Analyze traffic violation images using AI</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Send you automated analysis reports</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Store records for research and improvement purposes</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Comply with legal requirements</span>
          </li>
        </ul>
      </section>

      <section>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 rounded-lg bg-primary/10 text-primary">
            <Lock size={24} />
          </div>
          <h2 class="text-2xl font-bold">Data Storage & Security</h2>
        </div>
        <p class="text-muted-foreground leading-relaxed">
          Your data is stored securely in our database with industry-standard encryption.
          We implement appropriate technical and organizational measures to protect your information.
        </p>
      </section>

      <section>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 rounded-lg bg-primary/10 text-primary">
            <Shield size={24} />
          </div>
          <h2 class="text-2xl font-bold">Third-Party Services</h2>
        </div>
        <p class="text-muted-foreground mb-3">We use the following third-party services:</p>
        <div class="grid gap-3">
          <div class="p-4 rounded-lg border bg-card">
            <p class="font-semibold mb-1">WhatsApp Business API</p>
            <p class="text-sm text-muted-foreground">For messaging infrastructure</p>
          </div>
          <div class="p-4 rounded-lg border bg-card">
            <p class="font-semibold mb-1">Google Gemini</p>
            <p class="text-sm text-muted-foreground">For AI image analysis</p>
          </div>
          <div class="p-4 rounded-lg border bg-card">
            <p class="font-semibold mb-1">Supabase</p>
            <p class="text-sm text-muted-foreground">For secure data storage</p>
          </div>
        </div>
        <p class="text-muted-foreground mt-4">
          These services have their own privacy policies and we recommend reviewing them.
        </p>
      </section>

      <section>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 rounded-lg bg-primary/10 text-primary">
            <Users size={24} />
          </div>
          <h2 class="text-2xl font-bold">Your Rights</h2>
        </div>
        <p class="text-muted-foreground mb-3">You have the right to:</p>
        <ul class="space-y-2 text-muted-foreground">
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Access your personal data</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Request deletion of your data</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Opt-out of the service at any time</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>Request corrections to your data</span>
          </li>
        </ul>
      </section>

      <section>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 rounded-lg bg-primary/10 text-primary">
            <Mail size={24} />
          </div>
          <h2 class="text-2xl font-bold">Contact Us</h2>
        </div>
        <p class="text-muted-foreground leading-relaxed">
          For privacy-related inquiries or to exercise your rights, please contact us through
          the repository or affiliated university channels.
        </p>
      </section>
    </div>

    <div class="mt-12 text-center">
      <a href="/">
        <Button variant="outline" size="lg">
          <ArrowLeft size={20} />
          Back to Home
        </Button>
      </a>
    </div>
  </div>
</main>
