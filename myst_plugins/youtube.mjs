// MyST JavaScript plugin that provides a `youtube` directive.
// Usage in markdown:
//
// :::{youtube} 1peVp_IZ7Ts
// :width: 100%
// :height: 480
// :autoplay: 0
// :::

const youtubeDirective = {
  name: 'youtube',
  doc: 'Embed a YouTube video with sensible course defaults',
  alias: [],
  arg: {
    type: String,
    doc: 'YouTube video id or full url',
  },
  options: {
    width: { type: String, doc: 'Width, e.g. 100% or 640' },
    height: { type: String, doc: 'Height, e.g. 480' },
    autoplay: { type: Number, doc: 'autoplay=1 to start automatically' },
    controls: { type: Number, doc: 'controls parameter' },
    loop: { type: Number, doc: 'loop playback' },
    origin: { type: String, doc: 'origin for JS API security' },
  },
  run(data) {
    const raw = data.arg?.trim() ?? '';
    let vid = raw;
    if (raw.startsWith('http')) {
      // naive extraction
      const u = new URL(raw);
      if (u.searchParams.has('v')) vid = u.searchParams.get('v');
      else vid = u.pathname.split('/').filter(Boolean).pop();
    }

    // Default parameters for course embedding.
    const params = new URLSearchParams();
    // rel no longer fully disables related videos but can prefer same-channel
    params.set('rel', '0');
    // modestbranding deprecated but harmless to include
    params.set('modestbranding', '1');
    // disable annotations
    params.set('iv_load_policy', '3');
    // enable JS API so other course scripts can control playback if necessary
    params.set('enablejsapi', '1');

    if (data.options?.autoplay) params.set('autoplay', String(data.options.autoplay));
    if (data.options?.controls) params.set('controls', String(data.options.controls));
    if (data.options?.loop) params.set('loop', String(data.options.loop));
    if (data.options?.origin) params.set('origin', data.options.origin);

    const src = `https://www.youtube.com/embed/${vid}?${params.toString()}`;

    const width = data.options?.width ?? '100%';
    const height = data.options?.height ?? '480';

    const node = {
      type: 'html',
      value: `<div class="youtube-embed"><iframe src="${src}" width="${width}" height="${height}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`,
    };

    return [node];
  },
};

const plugin = { name: 'YouTube embed directive', directives: [youtubeDirective] };

export default plugin;
