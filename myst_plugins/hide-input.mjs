// Transform plugin that ensures all notebook code blocks carry the hide-input tag.

const toTagList = (value) => {
  if (Array.isArray(value)) return [...value];
  if (typeof value === 'string' && value.length > 0) return [value];
  return [];
};

const ensureTags = (data = {}) => {
  const tags = new Set([...toTagList(data.tags), 'hide-input']);
  return { ...data, tags: [...tags] };
};

const visit = (node) => {
  if (!node || typeof node !== 'object') return;

  if (node.type === 'block' && node.kind === 'notebook-code') {
    node.data = ensureTags(node.data);

    node.children?.forEach((child) => {
      if (child?.type === 'code') {
        child.data = ensureTags(child.data);
        if (child.visibility === 'show' || child.visibility === undefined) {
          child.visibility = 'hide';
        }
      }
    });
  }

  if (Array.isArray(node.children)) {
    node.children.forEach((child) => visit(child));
  }
};

export default {
  name: 'hide-input-tag-transform',
  transforms: [
    {
      name: 'hide-input-tag-transform',
      stage: 'document',
      plugin: () => (tree) => {
        visit(tree);
        return tree;
      },
    },
  ],
};
