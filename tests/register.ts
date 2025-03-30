import * as anchor from "@project-serum/anchor";
import fs from "fs";

const main = async () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const idl = JSON.parse(fs.readFileSync("target/idl/auth_product_registry.json", "utf8"));

  const programId = new anchor.web3.PublicKey("DUYDjC7h8GUFiBUeY25CRjQfokdeRdUCyC5AbPhZiBTi");
  const program = new anchor.Program(idl, programId, provider);

  const uid = [4, 162, 177, 195, 0, 159, 1]; // Example UID
  const metadata = "Nike Air Max 95 OG - Neon";

  const [productPda] = await anchor.web3.PublicKey.findProgramAddress(
    [Buffer.from("product"), Buffer.from(uid)],
    program.programId
  );

  await program.methods
    .registerProduct(uid, metadata)
    .accounts({
      product: productPda,
      authority: provider.wallet.publicKey,
      systemProgram: anchor.web3.SystemProgram.programId,
    })
    .rpc();

  console.log(" Product registered at:", productPda.toBase58());
};

main().catch((err) => {
  console.error(" Error:", err);
});

