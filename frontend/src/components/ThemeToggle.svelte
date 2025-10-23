<script lang="ts">
  import { themeManager } from "@/lib/theme.svelte";
  import { Sun, Moon } from "lucide-svelte";

  let isDark = $derived(themeManager.current === "dark");
</script>

<button
  onclick={() => themeManager.toggle()}
  class="fixed top-4 right-4 p-3 rounded-lg bg-card hover:bg-accent transition-all duration-200 shadow-md hover:shadow-lg border z-50 active:scale-95"
  aria-label="Toggle theme"
>
  {#if isDark}
    <Sun size={20} />
  {:else}
    <Moon size={20} />
  {/if}
</button>
