# debian-package-repo

APT package repository for PearOS, served via GitHub Pages at
[apt.pearos.xyz](https://apt.pearos.xyz).

## Structure

```
<arch>/<channel>/<release>/
```

- **Architectures**: `x86_64`, `aarch64`
- **Channels**:
  - `main` — stable packages
  - `testing` — pre-release / testing packages
- **Releases**: `latest`, `pahoe`, `monterey`, `catalina`, `mojave`, `big-sur`, `leopard`, `sierra`, `high-sierra`

Example: `x86_64/main/pahoe/`

## Pages

`index.html` files are generated automatically on every push by
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml),
which renders a directory listing ("Index of ...") for every folder and
deploys it via GitHub Pages. The generated pages are not committed to the
repo — they only exist in the deployed site.
