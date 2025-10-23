<script lang="ts">
  import { onMount } from 'svelte';
  import Home from './routes/Home.svelte';
  import Privacy from './routes/Privacy.svelte';
  import Reports from './routes/Reports.svelte';
  import NotFound from './routes/NotFound.svelte';

  let currentPath = $state(window.location.pathname);

  function navigate(event: MouseEvent) {
    const target = event.target as HTMLElement;
    const anchor = target.closest('a');
    
    if (anchor && anchor.href && anchor.origin === window.location.origin) {
      event.preventDefault();
      const url = new URL(anchor.href);
      window.history.pushState({}, '', url.pathname);
      currentPath = url.pathname;
    }
  }

  function handlePopState() {
    currentPath = window.location.pathname;
  }

  onMount(() => {
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  });
</script>

<svelte:window onclick={navigate} />

{#if currentPath === '/'}
  <Home />
{:else if currentPath === '/privacy'}
  <Privacy />
{:else if currentPath === '/reports'}
  <Reports />
{:else}
  <NotFound />
{/if}
