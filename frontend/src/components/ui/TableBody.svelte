<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
    class?: string;
  }

  let { children, class: className = "" }: Props = $props();
</script>

<tbody class="[&_tr:last-child]:border-0 {className}">
  {#if children}
    {@render children()}
  {/if}
</tbody>
