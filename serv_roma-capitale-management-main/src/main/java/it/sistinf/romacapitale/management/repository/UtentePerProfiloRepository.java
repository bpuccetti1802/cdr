package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.UtentePerProfiloEntity;
import org.springframework.stereotype.Repository;

@Repository
public class UtentePerProfiloRepository extends AbstractRepository<Long, UtentePerProfiloEntity> {

    public UtentePerProfiloRepository() {
        super(UtentePerProfiloEntity.class);
    }
}
