package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.UtentePerProfiloGetEntity;
import org.springframework.stereotype.Repository;

@Repository
public class UtentePerProfiloGetRepository extends AbstractRepository<Long, UtentePerProfiloGetEntity> {

    public UtentePerProfiloGetRepository() {
        super(UtentePerProfiloGetEntity.class);
    }
}
