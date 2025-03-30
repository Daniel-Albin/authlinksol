use anchor_lang::prelude::*;

declare_id!("DUYDjC7h8GUFiBUeY25CRjQfokdeRdUCyC5AbPhZiBTi");

#[program]
pub mod auth_product_registry {
    use super::*;

    pub fn register_product(ctx: Context<RegisterProduct>, uid: [u8; 7], metadata: String) -> Result<()> {
        let product = &mut ctx.accounts.product;
        product.uid = uid;
        product.metadata = metadata;
        product.authority = ctx.accounts.authority.key();
        Ok(())
    }

    pub fn verify_product(_ctx: Context<VerifyProduct>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(uid: [u8; 7])]
pub struct RegisterProduct<'info> {
    #[account(
        init,
        seeds = [b"product", &uid],
        bump,
        payer = authority,
        space = 8 + 7 + 4 + 256 + 32
    )]
    pub product: Account<'info, Product>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(uid: [u8; 7])]
pub struct VerifyProduct<'info> {
    #[account(seeds = [b"product", &uid], bump)]
    pub product: Account<'info, Product>,
}

#[account]
pub struct Product {
    pub uid: [u8; 7],
    pub metadata: String,
    pub authority: Pubkey,
}

