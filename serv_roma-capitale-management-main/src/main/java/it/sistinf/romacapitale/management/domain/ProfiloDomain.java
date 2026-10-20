package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.ProfiloPerAbilitazioneVO;
import it.sistinf.romacapitale.integration.management.vo.ProfiloVO;
import it.sistinf.romacapitale.management.entity.ProfiloEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.ProfiloMapper;
import it.sistinf.romacapitale.management.repository.ProfiloRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

@Service
@AllArgsConstructor
@Slf4j
public class ProfiloDomain extends AbstractDomain {

    private ProfiloMapper profiloMapper;
    private ProfiloRepository profiloRepository;

    private ProfiloPerAbilitazioneDomain profiloPerAbilitazioneDomain;
    private UtentePerProfiloDomain utentePerProfiloDomain;


    public ResponseListDTO<ProfiloVO> listProfili(RequestListDTO<ProfiloVO> request) throws ApplicationException {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<ProfiloEntity> results = null;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = profiloRepository.findAll(
                    hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(), EnumManagementDomainTypeFunction.GET_ALL_PROFILI_FILTERED
            );
            pageInfo =request.getPageInfo();
            totalCount = profiloRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_PROFILI_FILTERED_COUNT);
        }else{
            results = profiloRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_PROFILI_FILTERED);
            totalCount = (long)results.size();
        }

        ResponseListDTO<ProfiloVO> response = new ResponseListDTO<>();

        response.setList(profiloMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    public ProfiloVO profiloById(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Profilo");
        }

        return profiloMapper.mapTo(profiloRepository.findById(id));
    }

    public List<ProfiloPerAbilitazioneVO> createProfiloPerAbilitazione(List<ProfiloPerAbilitazioneVO> profiloPerAbilitazioneList, Long idProfilo) throws ApplicationException {
        List<ProfiloPerAbilitazioneVO> profiloPerAbilitazioneSavedlist = new ArrayList<>();

        int profiloDefaultCount = 0;
        for (ProfiloPerAbilitazioneVO profiloPerAbilitazioneVO : profiloPerAbilitazioneList) {
//            if("S".equals(utentePerProfiloVO.getProfiloDefault())){
//                profiloDefaultCount++;
//                if(profiloDefaultCount > 1){
//                    throw new ApplicationException("L'utente può avere un solo profilo di default");
//                }
//            }
            profiloPerAbilitazioneVO.getKey().setIdProfilo(idProfilo);
            profiloPerAbilitazioneDomain.createProfiloPerAbilitazione(profiloPerAbilitazioneVO);
            profiloPerAbilitazioneSavedlist.add(profiloPerAbilitazioneVO);
        }
        return profiloPerAbilitazioneSavedlist;
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public ProfiloVO createProfilo(ProfiloVO profiloVO) {
        if (ControlloCampi.campoVuoto(profiloVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(profiloVO.getDescrizione())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Descrizione Profilo");
        }
        ProfiloEntity entity = profiloMapper.mapFrom(profiloVO);

        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));

        profiloRepository.create(entity);
        //Inserimento valori su tabella profilo_per_abilitazione
        List<ProfiloPerAbilitazioneVO> profiloPerAbilitazioneSavedlist;
        if (profiloVO.getProfiloPerAbilitazioneList() != null && !profiloVO.getProfiloPerAbilitazioneList().isEmpty()) {
            profiloPerAbilitazioneSavedlist = createProfiloPerAbilitazione(profiloVO.getProfiloPerAbilitazioneList(), entity.getId());
        } else {
            throw new ApplicationException("La lista abilitazioni non può essere vuota");
        }
        profiloVO = profiloMapper.mapTo(entity);
        profiloVO.setProfiloPerAbilitazioneList(profiloPerAbilitazioneSavedlist);
        return profiloVO;
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public ProfiloVO updateProfilo(ProfiloVO profiloVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(profiloVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(profiloVO.getKey())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Key Profilo");
        }


        ProfiloEntity entity = profiloMapper.mapFrom(profiloVO);
        Long idProfilo = profiloVO.getKey();

        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setProfiloPerAbilitazioneList(null);
        profiloRepository.update(entity);

        //Aggiornamento abilitazione per profiloPerAbilitazione :cancello tutte le righe e le reinserisco
        profiloPerAbilitazioneDomain.deleteAllProfiloPerAbilitazioneByIdProfilo(idProfilo);

        List<ProfiloPerAbilitazioneVO> profiloPerAbilitazioneSavedlist;
        if (profiloVO.getProfiloPerAbilitazioneList() != null && !profiloVO.getProfiloPerAbilitazioneList().isEmpty()) {
            profiloPerAbilitazioneSavedlist = createProfiloPerAbilitazione(profiloVO.getProfiloPerAbilitazioneList(), entity.getId());
        } else {
            throw new ApplicationException("La lista Abilitazioni non può essere vuota");
        }
        profiloVO = profiloMapper.mapTo(entity);
        profiloVO.setProfiloPerAbilitazioneList(profiloPerAbilitazioneSavedlist);
        return profiloVO;
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public ProfiloVO deleteProfilo(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Profilo");
        }
        ProfiloEntity entity = profiloRepository.findById(id);

        //cancellazione dei dati su tabella utente_per_profilo associati al profilo da eliminare
        utentePerProfiloDomain.deleteAllUtentePerProfiloByIdProfilo(id);

        //cancellazione dei dati su tabella profilo_per_Abilitazione associati al profilo da eliminare
        profiloPerAbilitazioneDomain.deleteAllProfiloPerAbilitazioneByIdProfilo(id);

        profiloRepository.removeById(entity.getId());
        return profiloMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public List<ProfiloVO> recuperaRuoli(String cdAmbito, String cdApplicazione) throws ApplicationException {
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("cdAmbito", cdAmbito);
        hParams.put("cdApplicazione", cdApplicazione);
        List<ProfiloEntity> profili = profiloRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_PROFILI_BY_APPLICAZIONE);
        return profiloMapper.mapTo(profili);
    }

}
