package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.enums.SearchTypeEnum;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.exceptions.ObjectNotFoundException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.AESEncryptionUtils;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.core.vo.auth.LoginVO;
import it.sistinf.romacapitale.integration.management.vo.*;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntityPK;
import it.sistinf.romacapitale.management.entity.UtenteEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.ProfiloMapper;
import it.sistinf.romacapitale.management.mapper.UtenteMapper;
import it.sistinf.romacapitale.management.repository.ProfiloRepository;
import it.sistinf.romacapitale.management.repository.UtenteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class UtenteDomain extends AbstractDomain {

    private final UtenteMapper utenteMapper;

    private final ProfiloMapper profiloMapper;

    private final UtenteRepository utenteRepository;

    private final ProfiloRepository profiloRepository;

    private final UtentePerProfiloDomain utentePerProfiloDomain;

    private final ProfiloPerAbilitazioneDomain profiloPerAbilitazioneDomain;

    private final ApplicazioneDomain applicazioneDomain;
    private final UtentePerProfiloGetDomain utentePerProfiloGetDomain;

    @Value("${crittografiaPassword}")
    private String crittografiaPassword;

    @Value("${crittografiaSalt}")
    private String crittografiaSalt;


    public ResponseListDTO<UtenteVO> listUtenti(RequestListDTO<UtenteVO> request) throws ApplicationException {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<UtenteEntity> results = null;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = utenteRepository.findAll(
                    hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(), EnumManagementDomainTypeFunction.GET_ALL_UTENTI_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = utenteRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_UTENTI_FILTERED_COUNT);
        }else{
            results = utenteRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_UTENTI_FILTERED);
            totalCount = (long)results.size();
        }

        ResponseListDTO<UtenteVO> response = new ResponseListDTO<>();

        response.setList(utenteMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    public UtenteVO getUtente(Long id) throws ApplicationException {
        return utenteMapper.mapTo(utenteRepository.findById(id));
    }

    public List<UtenteVO> getUtenteByParams(RicercaUtenteVO ricercaUtenteVO){
        HashMap<String, Object> hParams = new HashMap<>();

        if(!ControlloCampi.campoVuoto(ricercaUtenteVO.getNome())){
            hParams.put("nome", ricercaUtenteVO.getNome());
            hParams.put("nomeSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(ricercaUtenteVO.getCognome())){
            hParams.put("cognome", ricercaUtenteVO.getCognome());
            hParams.put("cognomeSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(ricercaUtenteVO.getCodiceFiscale())){
            hParams.put("codiceFiscale", ricercaUtenteVO.getCodiceFiscale());
            hParams.put("codiceFiscaleSearchType", SearchTypeEnum.EQUALS.getSearchType());

        }
        if(!ControlloCampi.campoVuoto(ricercaUtenteVO.getUsername())){
            hParams.put("username", ricercaUtenteVO.getUsername());
            hParams.put("usernameSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        List<UtenteEntity> results = utenteRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_UTENTI_FILTERED);

        return utenteMapper.mapTo(results);
    }

    public List<UtentePerProfiloVO> createUtentePerProfilo(List<String> idProfiliUtenteList, Long idUtente) throws ApplicationException {
        List<UtentePerProfiloVO> utentePerProfiloSavedlist = new ArrayList<>();

        for (String idProfilo : idProfiliUtenteList) {

            UtentePerProfiloKeyVO utentePerProfiloKeyVO = new UtentePerProfiloKeyVO();
            utentePerProfiloKeyVO.setIdUtente(idUtente);
            utentePerProfiloKeyVO.setIdProfilo(Long.parseLong(idProfilo));

            UtentePerProfiloVO utentePerProfiloVO = new UtentePerProfiloVO();
            utentePerProfiloVO.setKey(utentePerProfiloKeyVO);
            utentePerProfiloVO.setProfilo(profiloMapper.mapTo(profiloRepository.findById(Long.parseLong(idProfilo))));

            utentePerProfiloDomain.createUtentePerProfilo(utentePerProfiloVO);

            utentePerProfiloSavedlist.add(utentePerProfiloVO);
        }
        return utentePerProfiloSavedlist;
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public UtenteVO createUtente(InserisciUtenteVO inserisciUtenteVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(inserisciUtenteVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(inserisciUtenteVO.getNome())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Nome Utente");
        }
        if (ControlloCampi.campoVuoto(inserisciUtenteVO.getCognome())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Cognome Utente");
        }
        if (ControlloCampi.campoVuoto(inserisciUtenteVO.getCodiceFiscale())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Codice Fiscale Utente");
        }
        if (ControlloCampi.campoVuoto(inserisciUtenteVO.getUsername())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Username");
        }

        UtenteEntity entity = utenteMapper.mapFrom(inserisciUtenteVO);
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("codiceFiscale", entity.getCodiceFiscale());
        try {
            UtenteEntity utenteDb = utenteRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_CODICEFISCALE);
            if (utenteDb != null) {
                throw new ApplicationException( "Esiste già un utente con codice fiscale: " + entity.getCodiceFiscale());
            }
        } catch (ObjectNotFoundException e) {
            log.debug("Nessun utente trovato con codice fiscale: {}", entity.getCodiceFiscale());
        }

        hParams = new HashMap<>();
        hParams.put("username", entity.getUsername());
        try {
            UtenteEntity utenteDb = utenteRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_USERNAME);
            if (utenteDb != null) {
                throw new ApplicationException("Esiste già un utente con username: " + entity.getUsername() + " , si prega di cambiare username");
            }
        } catch (ObjectNotFoundException e) {
            log.debug("Nessun utente trovato con username: {}", entity.getUsername());
        }

        if (!ControlloCampi.campoVuoto(inserisciUtenteVO.getPassword())){
            //Set della password criptata
            entity.setPassword(AESEncryptionUtils.encrypt(inserisciUtenteVO.getPassword(), crittografiaPassword, crittografiaSalt));
        }

        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));

        utenteRepository.create(entity);

        //Inserimento valori su tabella utente_per_profilo
        List<UtentePerProfiloVO> utentePerProfiloSavedlist;
        if (inserisciUtenteVO.getIdProfiloList() != null && !inserisciUtenteVO.getIdProfiloList().isEmpty()) {
            utentePerProfiloSavedlist = createUtentePerProfilo(inserisciUtenteVO.getIdProfiloList(), entity.getId());
        } else {
            throw new ApplicationException("La lista profili non può essere vuota");
        }
        UtenteVO utenteVO = utenteMapper.mapTo(entity);
        utenteVO.setUtentePerProfiloList(utentePerProfiloSavedlist); 
        return utenteVO;

    }


    @Transactional(propagation = Propagation.REQUIRED)
    public UtenteVO updateUtente(ModificaUtenteVO modificaUtenteVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(modificaUtenteVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(modificaUtenteVO.getKey())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Tecnico Utente");
        }

        Long idUtente = modificaUtenteVO.getKey();

        // Recupera l'entità esistente dal database
        UtenteEntity entity;
        try {
            entity = utenteRepository.findById(idUtente);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun utente trovato con id: " + idUtente);
        }

        // Aggiorna l'entità esistente con i valori del VO (preserva i campi non presenti nel VO)
        utenteMapper.updateEntityFromVO(modificaUtenteVO, entity);

        // Imposta i campi di audit
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));

        utenteRepository.update(entity);

        List<UtentePerProfiloVO> utentePerProfiloSavedlist  = null;
        if (modificaUtenteVO.getIdProfiloList() != null && !modificaUtenteVO.getIdProfiloList().isEmpty()) {
            // Aggiornamento profilo per utente per profilo: cancello tutte le righe e le reinserisco
            utentePerProfiloDomain.deleteAllUtentePerProfiloByIdUtente(idUtente);
            utentePerProfiloSavedlist = createUtentePerProfilo(modificaUtenteVO.getIdProfiloList(), entity.getId());
        }

        // Mappatura dell'entità aggiornata a VO da restituire
        UtenteVO newUtenteVO = utenteMapper.mapTo(entity);
        newUtenteVO.setUtentePerProfiloList(utentePerProfiloSavedlist != null
                ? utentePerProfiloSavedlist
                : new ArrayList<>());
        return newUtenteVO;
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public Boolean deleteUtente(Long id) throws ApplicationException {

        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Utente");
        }

        try {
            utenteRepository.findById(id);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun utente trovato con id: " + id);
        }

        try {
            //Cancellazione dei dati su tabella utente_per_profilo associati all'utente da eliminare
            utentePerProfiloDomain.deleteAllUtentePerProfiloByIdUtente(id);
            utenteRepository.removeById(id);
        } catch (ApplicationException e) {
            log.error("Errore nella cancellazione dell'utente con id: {}", id);
            log.error("Exception: ", e);
            return false;
        }

        return true;
    }

    public ProfileUserVO getUtenteAndAbilitazioniByUsername(LoginVO request) {
        ProfileUserVO profileUserVO = new ProfileUserVO();
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("username", request.getUsername());
        UtenteEntity utenteEntity = null;
        try {
            utenteEntity = utenteRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_USERNAME);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun utente trovato con username: " + request.getUsername());
        }
        profileUserVO.setUtente(utenteMapper.mapTo(utenteEntity));
        // recupero l'unione abilitazioni di tutti i profili relativi ad utente
        List<UtentePerProfiloVO> utentePerProfiloVOList = utentePerProfiloDomain.listUtentePerProfiloByIdUtente(utenteEntity.getId());
        getAbilitazioniFromProfiloList(request, utentePerProfiloVOList, profileUserVO);

        return profileUserVO;
    }

    private void getAbilitazioniFromProfiloList(LoginVO request, List<UtentePerProfiloVO> utentePerProfiloVOList, ProfileUserVO profileUserVO) throws ApplicationException {
        //Se Tipo di autorizzazione: G=Gruppo Applicazioni merge profili delle applicazioni figlie, P=Singolo profilo filtro solo per i profili dell'applicazione richiesta
        ApplicazioneEntityPK applicazioneEntityPK = new ApplicazioneEntityPK();
        applicazioneEntityPK.setCdApplicazione(request.getCdApplicazione());
        applicazioneEntityPK.setCdAmbito(request.getCdAmbito());
        ApplicazioneVO applicazioneVO = applicazioneDomain.getApplicazione(applicazioneEntityPK);
        List<UtentePerProfiloVO> profiliFiltrati;
        if ("G".equals(applicazioneVO.getTyAuth())) {
            //tipo Auth G=Gruppo Applicazioni, merge profili delle applicazioni figlie
            //trovo tutte le applicazioni figlie
            List<ApplicazioneVO> applicazioneFiglieList = applicazioneDomain.getApplicazioniFiglie(request.getCdAmbito(), request.getCdApplicazione());
            Set<String> idApplicazioniFiglieSet = estraiIdApplicazioniFiglie(applicazioneFiglieList); // Creo un Set per filtrare sulle applicazioni figlie
            //filtro tra tutti i profili dell'utente solo quelli relativi alle applicazioni figlie
            profiliFiltrati = utentePerProfiloVOList.stream()
                    .filter(u -> u != null && u.getProfilo() != null)
                    .filter(u -> {
                        String key = u.getProfilo().getCdApplicazione().trim() + "|" + u.getProfilo().getCdAmbito().trim();
                        return idApplicazioniFiglieSet.contains(key);
                    })
                    .collect(Collectors.toList());

        } else {
            //tipo Auth P=Singolo profilo, prendo solo i profili dello specifica applicazione passata in request
            profiliFiltrati = utentePerProfiloVOList.stream()
                    .filter(u -> u != null && u.getProfilo() != null)
                    .filter(u ->
                            request.getCdApplicazione().equals(u.getProfilo().getCdApplicazione()) &&
                                    request.getCdAmbito().equals(u.getProfilo().getCdAmbito())
                    )
                    .collect(Collectors.toList());
        }
        //prendo solo la lista di idProfilo filtrati in precedenza per ottenere la lista di abilitazioni tramite profiloPerAbilitazione
        List<Long> idProfiloList = profiliFiltrati.stream().map(utentePerProfiloVO -> utentePerProfiloVO.getKey().getIdProfilo()).toList();
        if (idProfiloList != null && !idProfiloList.isEmpty()) {
            //Lista di tutte le abilitazioni filtrate per lista profili
            List<ProfiloPerAbilitazioneVO> profiloPerAbilitazioneVOList = profiloPerAbilitazioneDomain.listProfiloPerAbilitazioneByProfiloList(idProfiloList);
            List<String> abilitazioni = profiloPerAbilitazioneVOList.stream().map(profiloPerAbilitazioneVO -> String.valueOf(profiloPerAbilitazioneVO.getAbilitazione().getCdAbilitazione())).toList();
            profileUserVO.setAbilitazioni(abilitazioni);
        } else {
            throw new ApplicationException("Nessun profilo trovato per l'utente con username: " + request.getUsername());
        }
    }

    public ProfileUserVO getUtenteAndAbilitazioniByUsernameAndStruttura(LoginVO request, String codStrutturaGet) {
        ProfileUserVO profileUserVO = new ProfileUserVO();
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("username", request.getUsername());
        UtenteEntity utenteEntity = null;
        try {
            utenteEntity = utenteRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_USERNAME);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun utente trovato con username: " + request.getUsername());
        }
        profileUserVO.setUtente(utenteMapper.mapTo(utenteEntity));
        // recupero l'unione abilitazioni di tutti i profili relativi ad utente e struttura
        List<UtentePerProfiloGetVO> utentePerProfiloGetVOList = utentePerProfiloGetDomain.listUtentePerProfiloGetByIdUtenteAndCodStruttura(utenteEntity.getId(),codStrutturaGet);
        //Creo un utentePerProfiloVOList partendo dal corrispettivo utentePerProfiloGetVOList
        List<UtentePerProfiloVO> utentePerProfiloVOList = utentePerProfiloGetVOList.stream()
                .map(utentePerProfiloGetVO -> {
                    UtentePerProfiloVO utentePerProfiloVO = new UtentePerProfiloVO();
                    utentePerProfiloVO.setProfilo(utentePerProfiloGetVO.getProfilo());
                    if (utentePerProfiloGetVO.getKey() != null) {
                        UtentePerProfiloKeyVO key = new UtentePerProfiloKeyVO();
                        key.setIdUtente(utentePerProfiloGetVO.getKey().getIdUtente());
                        key.setIdProfilo(utentePerProfiloGetVO.getKey().getIdProfilo());
                        utentePerProfiloVO.setKey(key);
                    }
                    return utentePerProfiloVO;
                })
                .collect(Collectors.toList());
        getAbilitazioniFromProfiloList(request, utentePerProfiloVOList, profileUserVO);

        return profileUserVO;
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public UtenteVO updateUtenteForLogin(UtenteVO utenteVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(utenteVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        UtenteEntity entity = utenteMapper.mapFrom(utenteVO);
        UtenteEntity utenteDb = utenteRepository.findById(entity.getId());
        Long idUtente = utenteVO.getKey();
        entity.setUltimoLogin(utenteVO.getUltimoLogin());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteInserimento(utenteDb.getUtenteInserimento());
        entity.setTimestampInserimento(utenteDb.getTimestampInserimento());
        utenteRepository.update(entity);
        return utenteMapper.mapTo(entity);
    }

    public Set<String> estraiIdApplicazioniFiglie(List<ApplicazioneVO> applicazioneFiglieList) {
        return applicazioneFiglieList.stream()
                .filter(app -> app.getKey() != null &&
                        app.getKey().getCdApplicazione() != null &&
                        app.getKey().getCdAmbito() != null)
                .map(app -> app.getKey().getCdApplicazione().trim() + "|" + app.getKey().getCdAmbito().trim())
                .collect(Collectors.toSet());
    }


    public List<UtenteVO> listUtentiPerRuolo(Long idProfilo) throws ApplicationException {
        List<Long> idUtenti = utentePerProfiloDomain.listIdUtentiPerRuolo(idProfilo);
        List<UtenteVO> utenti = new ArrayList<>();
        if(idUtenti != null) {
            for(Long id : idUtenti) {
                utenti.add(utenteMapper.mapTo(utenteRepository.findById(id)));
            }
        }

        return utenti;
    }

    public UtenteVO getUtenteByUsername(String username) throws ApplicationException {
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("username", username);
        hParams.put("usernameSearchType", "EQUALS");
        return utenteMapper.mapTo(utenteRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_USERNAME));
    }

    public ProfileUserVO getUtenteAndAbilitazioniByCodFiscale(LoginVO request) {
        ProfileUserVO profileUserVO = new ProfileUserVO();
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("codiceFiscale", request.getCodiceFiscale());
        UtenteEntity utenteEntity = null;
        try {
            utenteEntity = utenteRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_CODICEFISCALE);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun utente trovato con codiceFiscale: " + request.getCodiceFiscale());
        }
        profileUserVO.setUtente(utenteMapper.mapTo(utenteEntity));
        // recupero l'unione abilitazioni di tutti i profili relativi ad utente
        List<UtentePerProfiloVO> utentePerProfiloVOList = utentePerProfiloDomain.listUtentePerProfiloByIdUtente(utenteEntity.getId());
        getAbilitazioniFromProfiloList(request, utentePerProfiloVOList, profileUserVO);

        return profileUserVO;
    }

    public ProfileUserVO getUtenteAndAbilitazioniByCodFiscaleAndStruttura(LoginVO request, String codStrutturaGet) {
        ProfileUserVO profileUserVO = new ProfileUserVO();
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("codiceFiscale", request.getCodiceFiscale());
        UtenteEntity utenteEntity = null;
        try {
            utenteEntity = utenteRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_UTENTE_BY_CODICEFISCALE);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun utente trovato con codiceFiscale: " + request.getCodiceFiscale());
        }
        profileUserVO.setUtente(utenteMapper.mapTo(utenteEntity));
        // recupero l'unione abilitazioni di tutti i profili relativi ad utente e struttura
        List<UtentePerProfiloGetVO> utentePerProfiloGetVOList = utentePerProfiloGetDomain.listUtentePerProfiloGetByIdUtenteAndCodStruttura(utenteEntity.getId(),codStrutturaGet);
        //Creo un utentePerProfiloVOList partendo dal corrispettivo utentePerProfiloGetVOList
        List<UtentePerProfiloVO> utentePerProfiloVOList = utentePerProfiloGetVOList.stream()
                .map(utentePerProfiloGetVO -> {
                    UtentePerProfiloVO utentePerProfiloVO = new UtentePerProfiloVO();
                    utentePerProfiloVO.setProfilo(utentePerProfiloGetVO.getProfilo());
                    if (utentePerProfiloGetVO.getKey() != null) {
                        UtentePerProfiloKeyVO key = new UtentePerProfiloKeyVO();
                        key.setIdUtente(utentePerProfiloGetVO.getKey().getIdUtente());
                        key.setIdProfilo(utentePerProfiloGetVO.getKey().getIdProfilo());
                        utentePerProfiloVO.setKey(key);
                    }
                    return utentePerProfiloVO;
                })
                .collect(Collectors.toList());
        getAbilitazioniFromProfiloList(request, utentePerProfiloVOList, profileUserVO);

        return profileUserVO;
    }
}
