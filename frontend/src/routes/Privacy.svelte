<script lang="ts">
  import Card from "@/components/ui/Card.svelte";
  import CardHeader from "@/components/ui/CardHeader.svelte";
  import CardTitle from "@/components/ui/CardTitle.svelte";
  import CardContent from "@/components/ui/CardContent.svelte";
</script>

<main class="min-h-screen bg-linear-to-b from-background to-secondary/20 py-16">
  <div class="container max-w-3xl mx-auto px-4">
    <div class="mb-8">
      <h1 class="text-4xl font-bold tracking-tight mb-3">Privacy Policy</h1>
      <p class="text-muted-foreground">Last updated: October 2025</p>
    </div>

    <div class="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Overview</CardTitle>
        </CardHeader>
        <CardContent class="text-sm text-muted-foreground space-y-3">
          <p>
            This privacy policy explains how we collect, use, and protect your
            data when you interact with our Traffic Violation Analyzer service
            via WhatsApp.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Information We Collect</CardTitle>
        </CardHeader>
        <CardContent class="text-sm text-muted-foreground space-y-3">
          <p>When you use our service, we collect:</p>
          <ul class="list-disc pl-5 space-y-2">
            <li>Your WhatsApp phone number</li>
            <li>Images you send to us for analysis</li>
            <li>AI-generated analysis reports</li>
            <li>Timestamps of interactions</li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>How We Use Your Information</CardTitle>
        </CardHeader>
        <CardContent class="text-sm text-muted-foreground space-y-3">
          <p>We use your information to:</p>
          <ul class="list-disc pl-5 space-y-2">
            <li>Analyze traffic violation images using AI</li>
            <li>Send you automated analysis reports</li>
            <li>Store records for research and improvement purposes</li>
            <li>Comply with legal requirements</li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Data Storage & Security</CardTitle>
        </CardHeader>
        <CardContent class="text-sm text-muted-foreground space-y-3">
          <p>
            Your data is stored securely in our database with industry-standard
            encryption. We implement appropriate technical and organizational
            measures to protect your information.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Third-Party Services</CardTitle>
        </CardHeader>
        <CardContent class="text-sm text-muted-foreground space-y-3">
          <p>We use the following third-party services:</p>
          <ul class="list-disc pl-5 space-y-2">
            <li><strong>WhatsApp Business API</strong> - For messaging</li>
            <li><strong>Google Gemini</strong> - For AI image analysis</li>
            <li><strong>Supabase</strong> - For data storage</li>
          </ul>
          <p class="mt-3">
            These services have their own privacy policies and we recommend
            reviewing them.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your Rights</CardTitle>
        </CardHeader>
        <CardContent class="text-sm text-muted-foreground space-y-3">
          <p>You have the right to:</p>
          <ul class="list-disc pl-5 space-y-2">
            <li>Access your personal data</li>
            <li>Request deletion of your data</li>
            <li>Opt-out of the service at any time</li>
            <li>Request corrections to your data</li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Contact Us</CardTitle>
        </CardHeader>
        <CardContent class="text-sm text-muted-foreground">
          <p>
            For privacy-related inquiries or to exercise your rights, please
            contact us through the repository or affiliated university channels.
          </p>
        </CardContent>
      </Card>
    </div>

    <div class="mt-8 text-center">
      <a href="/" class="text-sm font-medium text-primary hover:underline">
        ← Back to Home
      </a>
    </div>
  </div>
</main>
