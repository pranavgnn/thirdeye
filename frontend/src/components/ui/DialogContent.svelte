<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
    class?: string;
  }

  let { children, class: className = "" }: Props = $props();
</script>

<div class="grid gap-4 {className}">
  {#if children}
    {@render children()}
  {/if}
</div>
