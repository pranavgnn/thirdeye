<script lang="ts">
  import Card from "@/components/ui/Card.svelte";
  import CardHeader from "@/components/ui/CardHeader.svelte";
  import CardTitle from "@/components/ui/CardTitle.svelte";
  import CardDescription from "@/components/ui/CardDescription.svelte";
  import CardContent from "@/components/ui/CardContent.svelte";
  import Alert from "@/components/ui/Alert.svelte";
  import AlertDescription from "@/components/ui/AlertDescription.svelte";
  import Badge from "@/components/ui/Badge.svelte";
</script>

<main class="min-h-screen bg-linear-to-b from-background to-secondary/20">
  <div class="container max-w-4xl mx-auto py-16 px-4">
    <div class="text-center mb-12">
      <h1 class="text-5xl font-bold tracking-tight mb-3">
        Traffic Violation Analyzer
      </h1>
      <p class="text-lg text-muted-foreground">
        AI-powered traffic violation detection via WhatsApp
      </p>
    </div>

    <div class="space-y-6">
      <Alert
        class="border-amber-200 bg-amber-50 dark:bg-amber-950/50 dark:border-amber-900"
      >
        <AlertDescription class="text-amber-900 dark:text-amber-200">
          <strong>Notice:</strong> This service is for educational purposes. All
          reports require manual verification by authorities.
        </AlertDescription>
      </Alert>

      <Card>
        <CardHeader>
          <CardTitle>How It Works</CardTitle>
          <CardDescription>Simple three-step process</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="flex items-start gap-4">
            <div
              class="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-semibold shrink-0"
            >
              1
            </div>
            <div>
              <h3 class="font-medium mb-1">Send Photo via WhatsApp</h3>
              <p class="text-sm text-muted-foreground">
                Submit an image of a traffic violation to our WhatsApp bot
              </p>
            </div>
          </div>
          <div class="flex items-start gap-4">
            <div
              class="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-semibold shrink-0"
            >
              2
            </div>
            <div>
              <h3 class="font-medium mb-1">AI Analysis</h3>
              <p class="text-sm text-muted-foreground">
                Our system analyzes the image using Google Gemini Vision
              </p>
            </div>
          </div>
          <div class="flex items-start gap-4">
            <div
              class="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-semibold shrink-0"
            >
              3
            </div>
            <div>
              <h3 class="font-medium mb-1">Receive Report</h3>
              <p class="text-sm text-muted-foreground">
                Get an instant summary with violation details and evidence
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Features</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div class="flex items-center gap-2 p-3 rounded-lg bg-secondary/50">
              <Badge variant="outline">AI</Badge>
              <span class="text-sm">Computer vision analysis</span>
            </div>
            <div class="flex items-center gap-2 p-3 rounded-lg bg-secondary/50">
              <Badge variant="outline">Fast</Badge>
              <span class="text-sm">Instant WhatsApp responses</span>
            </div>
            <div class="flex items-center gap-2 p-3 rounded-lg bg-secondary/50">
              <Badge variant="outline">Secure</Badge>
              <span class="text-sm">End-to-end encrypted</span>
            </div>
            <div class="flex items-center gap-2 p-3 rounded-lg bg-secondary/50">
              <Badge variant="outline">Private</Badge>
              <span class="text-sm">Data protection compliant</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Meta Business Verification</CardTitle>
        </CardHeader>
        <CardContent class="space-y-3">
          <p class="text-sm text-muted-foreground">
            This WhatsApp Business Account is verified by Meta and complies with
            their terms of service.
          </p>
          <div class="flex flex-wrap gap-2">
            <Badge>WhatsApp Business API</Badge>
            <Badge>Meta Verified</Badge>
            <Badge>GDPR Compliant</Badge>
          </div>
        </CardContent>
      </Card>

      <div class="flex justify-center gap-4 pt-4">
        <a
          href="/privacy"
          class="text-sm font-medium text-primary hover:underline"
        >
          Privacy Policy
        </a>
        <span class="text-muted-foreground">•</span>
        <a
          href="/reports"
          class="text-sm font-medium text-primary hover:underline"
        >
          View Reports
        </a>
      </div>
    </div>
  </div>
</main>
