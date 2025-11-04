<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
    class?: string;
  }

  let { children, class: className = "" }: Props = $props();
</script>

<thead class="[&_tr]:border-b {className}">
  {#if children}
    {@render children()}
  {/if}
</thead>
