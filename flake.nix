{
  description = "Hospital Information System — Emergency Department";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python311.withPackages (ps: with ps; [
          streamlit
          mysql-connector
        ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [ python ];

          shellHook = ''
            echo "🏥 HIS — Emergency Department dev shell"
            echo ""
            echo "Available commands:"
            echo "  streamlit run app.py    — Start the application"
            echo "  python db/setup_db.py   — Initialize database"
            echo ""
            echo "Environment variables (set these):"
            echo "  MYSQL_HOST      (default: localhost)"
            echo "  MYSQL_USER      (default: root)"
            echo '  MYSQL_PASSWORD  (default: empty)'
            echo "  MYSQL_DATABASE  (default: his_emergency)"
            echo ""
          '';
        };
      });
}
