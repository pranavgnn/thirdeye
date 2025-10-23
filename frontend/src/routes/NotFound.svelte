<script lang="ts">
  import Card from "@/components/ui/Card.svelte";
  import CardHeader from "@/components/ui/CardHeader.svelte";
  import CardTitle from "@/components/ui/CardTitle.svelte";
  import CardDescription from "@/components/ui/CardDescription.svelte";
  import CardContent from "@/components/ui/CardContent.svelte";
  import Button from "@/components/ui/Button.svelte";
</script>

<main
  class="min-h-screen bg-linear-to-b from-background to-secondary/20 flex items-center justify-center px-4"
>
  <Card class="max-w-md w-full border-2">
    <CardHeader class="text-center pb-4">
      <div class="mb-6 text-7xl font-bold text-muted-foreground/40">404</div>
      <CardTitle class="text-2xl mb-2">Page Not Found</CardTitle>
      <CardDescription>
        The page you're looking for doesn't exist or has been moved.
      </CardDescription>
    </CardHeader>
    <CardContent class="flex justify-center pt-2">
      <Button onclick={() => (window.location.href = "/")} class="min-w-32">
        Go Home
      </Button>
    </CardContent>
  </Card>
</main>
