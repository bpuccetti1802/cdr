package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.integration.management.vo.*;
import it.sistinf.romacapitale.integration.management.vo.requestVO.OperatoreRequestVO;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntityPK;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.UtenteMapper;
import it.sistinf.romacapitale.management.pman.dto.*;
import it.sistinf.romacapitale.management.pman.mapper.PmApplicazioneMapper;
import it.sistinf.romacapitale.management.pman.mapper.PmUtenteMapper;
import it.sistinf.romacapitale.management.pman.mapper.PmUtentePerProfiloMapper;
import it.sistinf.romacapitale.management.repository.ApplicazioneRepository;
import it.sistinf.romacapitale.management.repository.UtentePerProfiloRepository;
import it.sistinf.romacapitale.management.repository.UtenteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
@RequiredArgsConstructor
@Slf4j
public class OperatoreDomain extends AbstractDomain {


//    @Value("${idApplicazioni.attive}")
//    private String idApplicazioniAttive;

    private final UtenteRepository utenteRepository;
    private final UtentePerProfiloRepository utentePerProfiloRepository;
    private final  ApplicazioneRepository applicazioneRepository;

    private final UtenteMapper utenteMapper;
    private final PmUtenteMapper pmUtenteMapper;
    private final PmUtentePerProfiloMapper pmUtentePerProfiloMapper;
    private final PmApplicazioneMapper pmApplicazioneMapper;

    private final UtentePerProfiloDomain utentePerProfiloDomain;

    private final NodoPerVisibilitaDomain nodoPerVisibilitaDomain;
    private final ApplicazioneDomain applicazioneDomain;



    public OperatoreVO getOperatoreAndFunzioni(OperatoreRequestVO request) {

        OperatoreVO operatoreVO = new OperatoreVO();
        String lstCodEsterno = " ";
        HashMap<String, String> visibilitaOperatore;

        // creazione lista di stringhe partendo dalla stringa unica idApplicazioniAttive
//        List<String> idApplicazioniAttiveList = Arrays
//                .asList(idApplicazioniAttive.split(","));

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("codiceFiscale", request.getCodiceFiscale());

        UtenteVO utente = utenteMapper.mapTo(utenteRepository
                .findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_CODICEFISCALE));

        // lista filtrata per profilo con stesso idApplicazione
        List<UtentePerProfiloVO> resultsByApplicazione = utentePerProfiloDomain
                .listUtentePerProfiloByUtenteAndApplicazione(request.getIdApplicazione(),utente.getKey());

        // set dati utente
        utente.setUtentePerProfiloList(resultsByApplicazione);


        // recupero cdEsterno delle abilitazioni del Profilo
        Set<String> codEsternoList = new HashSet<>();


        for ( UtentePerProfiloVO vo : resultsByApplicazione ) {
            vo.getProfilo().getProfiloPerAbilitazioneList().stream()
                    .map(a -> a.getAbilitazione().getCdEsterno())
                    .forEach(codEsternoList::add);
        }

        // conversione  list --> stringa unica
        lstCodEsterno = String.join(", ", codEsternoList);

        visibilitaOperatore = nodoPerVisibilitaDomain.getVisibilitaUfficioMap(request.getIdNodo());

        // set dati operatore
        operatoreVO.setIdProfilo(request.getIdProfilo());
        operatoreVO.setIdApplicazioneSa(request.getIdApplicazione());
        operatoreVO.setUtente(utente);
        operatoreVO.setLstCodEsterno(lstCodEsterno);
        operatoreVO.setVisibilitaOperatore(visibilitaOperatore);
        return operatoreVO;
    }

    public OperatoreDTO getFunzioniOperatore() {

        OperatoreDTO operatoreDTO = new OperatoreDTO();
        String lstCodEsterno = " ";
        HashMap<String, String> visibilitaOperatore = null;


        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("codiceFiscale", getCurrentUser().getCodiceFiscale());

        // reupero Utente
        UtenteDTO utente = pmUtenteMapper.mapTo(utenteRepository
                .findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_CODICEFISCALE));



        // set lista Visibilita ( ex Filtri ) per ogni profilo dell utente
        for (UtentePerProfiloDTO up : utente.getUtentePerProfiloList()) {
            List<VisibilitaDTO> visibilitaList = new ArrayList<>();
            if (up.getNodoStruttura() != null) {
                for (NodoPerVisibilitaDTO nv : up.getNodoStruttura().getNodoPerVisibilitaList()) {
                    visibilitaList.add(nv.getVisibilita());
                }
                up.getNodoStruttura().setVisibilitaList(visibilitaList);
            }
        }

        // set Abilitazioni  ( ex Microfunzioni ) per ogni profilo dell utente
        for (UtentePerProfiloDTO up : utente.getUtentePerProfiloList()) {
            List<AbilitazioneDTO> abilitazioneList = new ArrayList<>();
            if (up.getProfilo() != null) {
                for (ProfiloPerAbilitazioneDTO pa : up.getProfilo().getProfiloPerAbilitazioneList()) {
                    abilitazioneList.add(pa.getAbilitazione());
                }
                up.getProfilo().setAbilitazioneList(abilitazioneList);
            }
        }

        //set lista profili dell'untente
        utente.setUtentePerProfiloList(utente.getUtentePerProfiloList());


        // recupero cdEsterno delle abilitazioni del Profilo
        Set<String> codEsternoList = new HashSet<>();
        for ( UtentePerProfiloDTO up : utente.getUtentePerProfiloList() ) {
            up.getProfilo().getProfiloPerAbilitazioneList().stream()
                    .map(a -> a.getAbilitazione().getCdEsterno())
                    .forEach(codEsternoList::add);
        }


        // conversione  list --> stringa unica
        lstCodEsterno = String.join(", ", codEsternoList);

        //recupero applicazioneDTO
//        ApplicazioneEntityPK key = new ApplicazioneEntityPK();
//        key.setCdAmbito(getCurrentUser().getCdAmbito());
//        key.setCdApplicazione(getCurrentUser().getCdApplicazione());
//        ApplicazioneDTO applicazione = recuperoApplicazione(key);

        // set dati operatore
//        operatoreDTO.setIdProfilo(Long.valueOf(getCurrentUser().getIdProfilo()));
//        operatoreDTO.setIdApplicazioneSa(applicazione.getIdApplicazioneSa());
        operatoreDTO.setUtente(utente);
        operatoreDTO.setLstCodEsterno(lstCodEsterno);
        operatoreDTO.setVisibilitaOperatore(visibilitaOperatore);
        return operatoreDTO;

    }



    public ApplicazioneDTO recuperoApplicazione(ApplicazioneEntityPK id) throws ApplicationException {
        return pmApplicazioneMapper.mapTo(applicazioneRepository.findById(id));
    }




}
