package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
@Slf4j
public class ManutenzioneDomain extends AbstractDomain {

    public void write(String cdAmbito, String cdApplicazione, Boolean isInManutenzione) {
        writeCache(this.getKey(cdAmbito, cdApplicazione), isInManutenzione);
    }

    public Boolean read(String cdAmbito, String cdApplicazione) {
        return readFromCache(this.getKey(cdAmbito, cdApplicazione));
    }

    private String getKey(String cdAmbito, String cdApplicazione){
        return cdAmbito + '-' + cdApplicazione;
    }
}
