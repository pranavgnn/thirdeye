<script lang="ts">
  import Button from "@/components/ui/Button.svelte";
  import { Home, AlertCircle } from "lucide-svelte";
</script>

<main class="min-h-screen flex items-center justify-center px-4">
  <div class="text-center max-w-md">
    <div class="mb-8">
      <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-muted mb-6">
        <AlertCircle size={48} class="text-muted-foreground" />
      </div>
      <div class="text-8xl font-bold text-muted-foreground/40 mb-4">404</div>
      <h1 class="text-3xl font-bold mb-3">Page Not Found</h1>
      <p class="text-lg text-muted-foreground mb-8">
        The page you're looking for doesn't exist or has been moved.
      </p>
    </div>
    <Button size="lg" onclick={() => window.location.href = "/"}>
      <Home size={20} />
      Go Home
    </Button>
  </div>
</main>
