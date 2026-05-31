{
  description = "Prometheus exporter for nvtop";

  nixConfig = {
    extra-substituters = [
      "https://nix.trev.zip"
    ];
    extra-trusted-public-keys = [
      "trev:I39N/EsnHkvfmsbx8RUW+ia5dOzojTQNCTzKYij1chU="
    ];
  };

  inputs = {
    systems.url = "github:nix-systems/default";
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    trev = {
      url = "github:spotdemo4/nur";
      inputs.systems.follows = "systems";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      trev,
      ...
    }:
    trev.libs.mkFlake (
      system: pkgs: {
        devShells = {
          default = pkgs.mkShell {
            shellHook = pkgs.shellhook.ref;
            packages = with pkgs; [
              # python
              python314
              uv

              # deps
              nvtopPackages.full

              # lint
              ruff
              nixd
              nil

              # format
              nixfmt
              prettier

              # util
              bumper
              flake-release
            ];
          };

          bump = pkgs.mkShell {
            packages = with pkgs; [
              bumper
            ];
          };

          release = pkgs.mkShell {
            packages = with pkgs; [
              flake-release

              # python
              python314
              uv
            ];
          };

          update = pkgs.mkShell {
            packages = with pkgs; [
              renovate

              # python
              python314
              uv
            ];
          };

          vulnerable = pkgs.mkShell {
            packages = with pkgs; [
              pysentry # python
              flake-checker # flake
              zizmor # actions
            ];
          };
        };

        apps = pkgs.mkApps {
          default = "uv run nvtop-exporter";
        };

        checks = pkgs.mkChecks {
          python = {
            src = self.packages.${system}.default;
            packages = with pkgs; [
              ruff
            ];
            script = ''
              ruff check
            '';
          };

          nix = {
            root = ./.;
            filter = file: file.hasExt "nix";
            packages = with pkgs; [
              nixfmt
            ];
            forEach = ''
              nixfmt --check "$file"
            '';
          };

          renovate = {
            root = ./.github;
            files = ./.github/renovate.json;
            packages = with pkgs; [
              renovate
            ];
            script = ''
              renovate-config-validator renovate.json
            '';
          };

          actions = {
            root = ./.;
            files = ./.github/workflows;
            packages = with pkgs; [
              action-validator
              zizmor
            ];
            forEach = ''
              action-validator "$file"
              zizmor "$file"
            '';
          };

          prettier = {
            root = ./.;
            filter = file: file.hasExt "yaml" || file.hasExt "json" || file.hasExt "md";
            packages = with pkgs; [
              prettier
            ];
            forEach = ''
              prettier --check "$file"
            '';
          };
        };

        formatter = pkgs.treefmt.withConfig {
          configFile = ./treefmt.toml;
          runtimeInputs = with pkgs; [
            ruff
            nixfmt
            prettier
          ];
        };

        packages.default = pkgs.python314Packages.buildPythonPackage (
          final: with pkgs.lib; {
            pname = "nvtop-exporter";
            version = "0.0.10";

            src = fileset.toSource {
              root = ./.;
              fileset = fileset.unions [
                ./.python-version
                ./LICENSE
                ./pyproject.toml
                ./README.md
                ./uv.lock
                ./src
              ];
            };

            pyproject = true;
            build-system = with pkgs.python314Packages; [
              setuptools
              uv-build-latest
            ];

            pythonRelaxDeps = true;
            dependencies = with pkgs.python314Packages; [
              prometheus-client
              pydantic
            ];

            buildInputs = with pkgs; [
              nvtopPackages.full
            ];

            makeWrapperArgs = [
              "--prefix PATH : ${pkgs.nvtopPackages.full}/bin"
            ];

            meta = {
              mainProgram = "nvtop-exporter";
              description = "Prometheus exporter for nvtop";
              license = licenses.mit;
              platforms = platforms.all;
              homepage = "https://github.com/spotdemo4/nvtop-exporter";
              changelog = "https://github.com/spotdemo4/nvtop-exporter/releases/tag/v${final.version}";
            };
          }
        );

        images.default = pkgs.mkImage {
          src = self.packages.${system}.default;
          contents = with pkgs; [ dockerTools.caCertificates ];
          config.ExposedPorts = {
            "8080/tcp" = { };
          };
        };

        appimages.default = pkgs.mkAppImage {
          src = self.packages.${system}.default;
        };
      }
    );
}
