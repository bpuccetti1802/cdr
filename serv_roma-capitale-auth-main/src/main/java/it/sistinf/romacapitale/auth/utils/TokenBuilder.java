package it.sistinf.romacapitale.auth.utils;


import it.sistinf.romacapitale.core.security.CurrentUser;
import it.sistinf.romacapitale.core.security.JwtManager;
import it.sistinf.romacapitale.integration.management.vo.IdTokenDecodificato;
import it.sistinf.romacapitale.integration.management.vo.ProfileUserVO;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.UUID;

/**
* Classe TokenBuilder
*/
@Service
@AllArgsConstructor
@Slf4j
public class TokenBuilder {

    private final JwtManager jwtManager;

    public String prepareToken(ProfileUserVO profileUserVO, boolean reduced) {

        //Preparo una classe con i claim del token
        CurrentUser cu = prepareCurrentUser(profileUserVO);
        if (reduced) {
            cu.setAuthorities(new ArrayList<>());
        } else {
            cu.setAuthorities(profileUserVO.getAbilitazioni());
        }
        String token = jwtManager.createToken(cu);
        cu.setToken(token);

        return token;
    }

    private CurrentUser prepareCurrentUser(ProfileUserVO authuser) {
        CurrentUser cu = new CurrentUser();
        if (authuser.getUtente() != null){
            cu.setUsername(authuser.getUtente().getUsername());
            cu.setNome(authuser.getUtente().getNome());
            cu.setCognome(authuser.getUtente().getCognome());
            cu.setCodiceFiscale(authuser.getUtente().getCodiceFiscale());
        }
        if (authuser.getSessionId() != null) {
            cu.setSessionId(authuser.getSessionId());
        } else {
            cu.setSessionId(UUID.randomUUID()+"");
        }
        if (authuser.getCdAmbito() != null){
            cu.setCdAmbito(authuser.getCdAmbito());
        }
        if (authuser.getCdApplicazione() != null){
            cu.setCdApplicazione(authuser.getCdApplicazione());
        }

//      if (authuser.getProfilo() != null ) {
//            cu.setIdProfilo(authuser.getProfilo().getKey().toString());
//            //la lista profili non viene settata nel token
//      }

        //FgListaStrutture
        if (authuser.getFgListaStrutture() != null){
            cu.setFgListaStrutture(authuser.getFgListaStrutture());
        }

        //FlagTokenReduced
        if (authuser.getFlagTokenReduced() != null){
            cu.setFlagTokenReduced(authuser.getFlagTokenReduced());
        }

        if (authuser.getStruttura()!= null){
            cu.setCodStruttura(authuser.getStruttura().getNmStruttura());
            cu.setDescStruttura(authuser.getStruttura().getDsStruttura());
        }

        //campi IAM
        if (authuser.getOidcVO() != null && authuser.getOidcVO().getIdTokenDecodificato() != null) {
            IdTokenDecodificato idToken = authuser.getOidcVO().getIdTokenDecodificato();

            cu.setIV_ASS_UID(idToken.getIV_ASS_UID());
            cu.setIV_ASS_CODFIS(idToken.getIV_ASS_CODFIS());
            cu.setIV_PG_CODFIS(idToken.getIV_PG_CODFIS());
            cu.setIV_PG_PIVA(idToken.getIV_PG_PIVA());
            cu.setIV_PG_RAG_SOC(idToken.getIV_PG_RAG_SOC());
            cu.setIV_PG_NATURA(idToken.getIV_PG_NATURA());
            cu.setIV_PG_NREA(idToken.getIV_PG_NREA());
            cu.setIV_PG_CCIAA(idToken.getIV_PG_CCIAA());
            cu.setIV_PG_UID(idToken.getIV_PG_UID());
            cu.setIV_PG_INDIRIZZO(idToken.getIV_PG_INDIRIZZO());
            cu.setIV_PG_CIV_IND(idToken.getIV_PG_CIV_IND());
            cu.setIV_PG_ESP_IND(idToken.getIV_PG_ESP_IND());
            cu.setIV_PG_COM_IND(idToken.getIV_PG_COM_IND());
            cu.setIV_PG_CAP_IND(idToken.getIV_PG_CAP_IND());
            cu.setIV_PG_PROV_IND(idToken.getIV_PG_PROV_IND());
            cu.setIV_PG_MAIL(idToken.getIV_PG_MAIL());
            cu.setIV_PG_MAIL_PEC(idToken.getIV_PG_MAIL_PEC());
            cu.setIV_PG_TELEFONO(idToken.getIV_PG_TELEFONO());
            cu.setIV_PG_MOBILE(idToken.getIV_PG_MOBILE());
            cu.setIV_PG_RUOLO(idToken.getIV_PG_RUOLO());
            cu.setIV_PG_CONSENSO_GDPR(idToken.getIV_PG_CONSENSO_GDPR());
            cu.setIV_PG_CATEGORIA(idToken.getIV_PG_CATEGORIA());
            cu.setIV_CODFIS(idToken.getIV_CODFIS());
            cu.setIV_NOME(idToken.getIV_NOME());
            cu.setIV_COGNOME(idToken.getIV_COGNOME());
            cu.setIV_NASCITA_DATA(idToken.getIV_NASCITA_DATA());
            cu.setIV_SEX(idToken.getIV_SEX());
            cu.setIV_NASCITA_COMUNE(idToken.getIV_NASCITA_COMUNE());
            cu.setIV_NASCITA_NAZIONE(idToken.getIV_NASCITA_NAZIONE());
            cu.setIV_RES_VIA(idToken.getIV_RES_VIA());
            cu.setIV_RES_CIVICO(idToken.getIV_RES_CIVICO());
            cu.setIV_RES_EDIFICIO(idToken.getIV_RES_EDIFICIO());
            cu.setIV_RES_LOTTO(idToken.getIV_RES_LOTTO());
            cu.setIV_RES_COMUNE(idToken.getIV_RES_COMUNE());
            cu.setIV_RES_PROV(idToken.getIV_RES_PROV());
            cu.setIV_RES_CAP(idToken.getIV_RES_CAP());
            cu.setIV_RES_NAZIONE(idToken.getIV_RES_NAZIONE());
            cu.setIV_EMAIL(idToken.getIV_EMAIL());
            cu.setIV_MAILP(idToken.getIV_MAILP());
            cu.setIV_TEL(idToken.getIV_TEL());
            cu.setIV_CELL(idToken.getIV_CELL());
            cu.setIV_USER(idToken.getIV_USER());
//            cu.setCdAmbito(idToken.getCd_ambito());
            // --- scope anagrafica ---
            cu.setIv_nascita_prov(idToken.getIv_nascita_prov());
            // --- persona giuridica ---
            cu.setIv_pg_delega(idToken.getIv_pg_delega());
            cu.setIv_pg_ruolo_cod(idToken.getIv_pg_ruolo_cod());
            cu.setIv_pg_categoria_cod(idToken.getIv_pg_categoria_cod());
            // --- attributi delega ---
            cu.setIv_dg_iat(idToken.getIv_dg_iat());
            cu.setIv_dg_exp(idToken.getIv_dg_exp());
            cu.setIv_dg_nbf(idToken.getIv_dg_nbf());
            cu.setIv_dg_services(idToken.getIv_dg_services());
            cu.setIv_dg_id(idToken.getIv_dg_id());
            cu.setIv_dg_cognome(idToken.getIv_dg_cognome());
            cu.setIv_dg_codfis(idToken.getIv_dg_codfis());
            cu.setIv_dg_nome(idToken.getIv_dg_nome());
            cu.setIv_dg_telefono(idToken.getIv_dg_telefono());
            // --- residenza ---
            cu.setIv_res_int(idToken.getIv_res_int());
            cu.setIv_res_scala(idToken.getIv_res_scala());
            // --- domicilio ---
            cu.setIv_dom_via(idToken.getIv_dom_via());
            cu.setIv_dom_comune(idToken.getIv_dom_comune());
            cu.setIv_dom_prov(idToken.getIv_dom_prov());
            cu.setIv_dom_cap(idToken.getIv_dom_cap());
            // --- assistito ---
            cu.setIv_ass_rag_soc(idToken.getIv_ass_rag_soc());
        }

        cu.getAuthorities().addAll(authuser.getAbilitazioni());
        return cu;
    }
}
