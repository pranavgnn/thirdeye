<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
    class?: string;
  }

  let { children, class: className = "" }: Props = $props();
</script>

<div class="w-full overflow-auto">
  <table class="w-full caption-bottom text-sm {className}">
    {#if children}
      {@render children()}
    {/if}
  </table>
</div>
