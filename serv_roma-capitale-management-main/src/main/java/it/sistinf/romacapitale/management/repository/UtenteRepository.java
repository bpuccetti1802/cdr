package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.UtenteEntity;
import org.springframework.stereotype.Repository;

@Repository
public class UtenteRepository extends AbstractRepository<Long, UtenteEntity> {

    public UtenteRepository() {
        super(UtenteEntity.class);
    }
}
