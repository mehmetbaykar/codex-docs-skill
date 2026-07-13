---
title: Image generation
source: https://learn.chatgpt.com/docs/image-generation
path: /docs/image-generation
---

# Image generation

Ask ChatGPT to generate or edit images. Use image generation for UI assets,
banners, backgrounds, illustrations, sprite sheets, and placeholders you want
to create alongside code or in a ChatGPT conversation.

Ask for an image from the app composer. Add a reference image when you want
ChatGPT to transform an existing asset or use it as visual guidance.

## Generate or edit an image

Describe the image in natural language. Add a reference image when you want
ChatGPT to transform or extend an existing asset.

Include `$imagegen` in your prompt to invoke the image generation skill
explicitly.

Built-in image generation uses `gpt-image-2` and counts toward your general
Codex usage limits. Image generations use included limits 3–5x faster on
average than similar turns without image generation, depending on image quality
and size. For larger batches, set `OPENAI_API_KEY` in your environment and ask
ChatGPT to generate images through the API so API pricing applies.

## Write effective image prompts

A useful image prompt is often only one to three clear sentences. Describe the
details that determine whether the result succeeds:

- Explain the image's purpose or intended audience.
- Name the main subject and what is happening.
- Describe the setting, composition, and visual style.
- Add framing, dimensions, lighting, colors, or materials when they matter.
- State constraints, including anything the image must not contain.

Prefer concrete visual language over broad reactions. For example, describe
where light comes from instead of asking for “beautiful lighting.” Repeat any
requirement that must stay fixed.

## Refine the result

Start with the core idea, then make small, targeted revisions. Adjust one
element at a time so the composition and other important details do not drift.
You can also select a specific area of an image and describe the change for that
area.

When editing an existing image, say exactly what should change and what must
stay the same.

For broader revisions, keep the feedback direct and actionable: make the image
brighter, reduce the color saturation, simplify the background, or keep the
composition while changing the style.

## Use multiple reference images

Use a small set of reference images when one image defines the content and
another defines the style, layout, or other visual direction. Identify each
image by order and explain how the images relate. Use spatial terms such as
foreground, background, left, and right when combining elements.

## Add text to an image

Keep in-image text short and specify it precisely. Put the exact text in
quotation marks, preserve the capitalization you want, and describe its font
style, size, color, and placement. For an uncommon name, spell out the letters
when accuracy matters. State whether any other text is allowed.

## Create infographics and dense layouts

Image generation can help draft explainers, posters, labeled diagrams,
timelines, and other information-rich visuals. Describe the information
hierarchy and layout, keep labels concise, and request sharp text rendering.
For dense copy or production-critical typography, review every word and finish
the asset in a design tool when needed.

## Additional considerations

- **Use likenesses with care.** When depicting a real person, provide a
  reference photo when appropriate and confirm that you have permission to use
  their likeness.
- **Ask for an original treatment.** Request a generic or original design
  instead of imitating a specific brand, product, artist, or artwork.
- **Credit is optional.** You do not need to credit OpenAI for generated images,
  though you can explain how an asset was made when that context is useful.
- **Follow applicable policies.** Use images in accordance with your
  organization's guidelines and [OpenAI's usage
  policies](https://openai.com/policies/usage-policies/).

## Related docs

- [Codex pricing](https://learn.chatgpt.com/docs/pricing#image-generation-usage-limits)
- [Image inputs](https://learn.chatgpt.com/docs/image-inputs)
- [Image generation API guide](https://developers.openai.com/api/docs/guides/image-generation)
- [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer)
- [Creating images with ChatGPT](https://openai.com/academy/image-generation/)

[
    Explore more image generation prompts and results.
