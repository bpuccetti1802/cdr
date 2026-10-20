package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.management.entity.ConfigurazioneEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.repository.ConfigurazioneRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;

@Service
@AllArgsConstructor
@Slf4j
public class ConfigurazioneDomain extends AbstractDomain {

    private Environment environment;

    private ConfigurazioneRepository configurazioneRepository;

    public ResponseDTO<HashMap<String,String>> getProperties(String cdAmbito, String cdApplicazione) throws ApplicationException {

        HashMap<String,String> response = new HashMap<>();

        HashMap<String,Object> hParam = new HashMap<>();

        hParam.put("cdAmbito", cdAmbito);
        hParam.put("cdApplicazione", cdApplicazione);

        List<ConfigurazioneEntity> properties = configurazioneRepository.findAll(hParam, EnumManagementDomainTypeFunction.GET_ALL_PARAM_BY_APLICATION_AND_AMBITO);

        for(ConfigurazioneEntity configurazione : properties){
            if("S".equals(configurazione.getTyParametro())){
                response.put(configurazione.getId().getDesNomeParametro(), environment.getProperty(configurazione.getId().getDesNomeParametro()));
            }else{
                response.put(configurazione.getId().getDesNomeParametro(), configurazione.getDesValParametro());
            }
        }

        return new ResponseDTO<>(response);
    }

}
