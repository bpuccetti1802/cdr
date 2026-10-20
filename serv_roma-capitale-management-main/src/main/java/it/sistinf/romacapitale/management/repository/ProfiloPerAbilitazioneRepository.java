package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.ProfiloPerAbilitazioneEntity;
import org.springframework.stereotype.Repository;

@Repository
public class ProfiloPerAbilitazioneRepository extends AbstractRepository<Long, ProfiloPerAbilitazioneEntity> {

    public ProfiloPerAbilitazioneRepository() {
        super(ProfiloPerAbilitazioneEntity.class);
    }
}
